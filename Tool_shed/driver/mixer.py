import argparse
import os
from collections import defaultdict
import json

script_path = os.path.dirname(os.path.realpath(__file__))

def base3(n: int) -> str:
    if n == 0:
        return '0'
    digits = []
    while n:
        digits.append(str(n % 3))
        n //= 3
    return ''.join(reversed(digits))

def mixer(benchmark):
    file_contents = {}
    # open the benchmark files from ../../Benchmark/{benchmark}/{untyped,shallow,advanced}
    with open(f'{script_path}/../../Benchmark/{benchmark}/untyped/main.py', 'r') as f:
        file_contents["untyped"] = f.read()
    with open(f'{script_path}/../../Benchmark/{benchmark}/shallow/main.py', 'r') as f:
        file_contents["shallow"] = f.read()
    with open(f'{script_path}/../../Benchmark/{benchmark}/advanced/main.py', 'r') as f:
        file_contents["advanced"] = f.read()
    
    # partition the files around "### SECTION SEPARATOR ###" and save the partitions
    partitions = defaultdict(dict)
    for section in file_contents:
        for i, partition in enumerate(file_contents[section].split('### SECTION SEPARATOR ###')):
            partitions[i][section] = partition

    # now yield all possible combinations of partitions
    key = {
        0: "untyped",
        1: "shallow",
        2: "advanced"
    }
    for i in range(3 ** len(partitions) - 1):
        selection = base3(i).zfill(len(partitions) - 1)        
        metadata = {
            "selection": selection,
            "ratios": {
                "untyped": 0,
                "shallow": 0,
                "advanced": 0
            }
        }

        combination = partitions[0]["advanced"]
        for j in range(len(partitions)-1):             
            segment = partitions[j+1][key[int(selection[j])]]
            combination += segment

            untyped_segment = partitions[j+1]["untyped"]
            metadata["ratios"][key[int(selection[j])]] += len(untyped_segment)
        
        total = sum(metadata["ratios"].values())
        metadata["ratios"]["advanced"] /= total
        metadata["ratios"]["shallow"] /= total
        metadata["ratios"]["untyped"] /= total
        
        yield combination, metadata

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('benchmark', type=str, help='Benchmark to run')
    parser.add_argument('n', type=int, help='Number of iterations')
    args = parser.parse_args()
    
    # create a temporary directory to store the benchmark files
    os.makedirs(f'{script_path}/temp', exist_ok=True)
    
    # refresh the results file
    os.makedirs(f'{script_path}/results', exist_ok=True)
    with open(f'{script_path}/results/{args.benchmark}.jsonl', 'w') as f:
        pass
    
    for combination, metadata in mixer(args.benchmark):
        # write the combination to a file
        with open(f'{script_path}/temp/main.py', 'w') as f:
            f.write(combination)
        
        try:
            # run the benchmark and timeout after 10 * args.n seconds
            out = os.popen(f'timeout {10 * args.n}s python {script_path}/temp/main.py {args.n}').read()
            time = float(out)
            metadata["time"] = time
            
            # save the metadata to results/{benchmark}.json
            with open(f'{script_path}/results/{args.benchmark}.jsonl', 'a') as f:
                f.write(json.dumps(metadata) + '\n')
        except ValueError:
            pass
    
    # delete the temporary directory and its contents
    os.system(f'rm -r {script_path}/temp')
