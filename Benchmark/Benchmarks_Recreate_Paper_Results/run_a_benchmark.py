import csv
import subprocess
import time
import os

def run_commands_and_record_runtimes(benchmark_name, commands, metric_name, num_runs, final_itr_arg):

    directory_name = "benchmark_runtime_records"
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    csv_filename = os.path.join(directory_name, f"{benchmark_name}_{metric_name}_runtimes.csv")
    
    
    with open(csv_filename, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        
        if metric_name == "tmax":
            header = ["Iteration"] + ["T-Max (SP JIT SF)","T-Max (SP JIT)","T-Max (SP)","T-Max (JIT SF)","T-Max (JIT)","T-Max ()" ]
        elif metric_name == "tmin":
            header = ["Iteration"] + ["T-Min (SP JIT SF)","T-Min (SP JIT)","T-Min (SP)","T-Min (JIT SF)","T-Min (JIT)","T-Min ()" ]
        else:
            header = ["Iteration"] + ["Orig (JIT SF)","Orig (JIT)","Orig ()"]
        
        csv_writer.writerow(header)

        for run in range(num_runs):
            runtimes = [f"Iteration {run+1}"]

            for command in commands:
                command_with_name = command.format(benchmark_name=benchmark_name,final_itr_arg = final_itr_arg)

                start_time = time.time()
                process = subprocess.Popen(command_with_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                process.communicate()
                end_time = time.time()

                runtime = round(end_time - start_time,3)
                runtimes.append(runtime)

            csv_writer.writerow(runtimes)

    print(f"Command runtimes recorded in {csv_filename}")


def normalize_csv(filename, normalizer_metric):
    data = []
    with open(filename, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data.append(row)
    
    normalized_filename = os.path.join("benchmark_runtime_records", f"normalized_{os.path.basename(filename)}")
 
    with open(normalized_filename, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        
        header = data[0]
        csv_writer.writerow(header)

        tmax_column_index = header.index(f"{normalizer_metric} (SP JIT SF)")

        for row in data[1:]:
            normalized_row = [row[0]]
            tmax_value = float(row[tmax_column_index])
            
            for value in row[1:]:
                normalized_value = round(float(value) / tmax_value, 2)
                normalized_row.append(normalized_value)
            
            csv_writer.writerow(normalized_row)

    print(f"CSV file normalized and saved as {normalized_filename}")



if __name__ == "__main__":

    while True:
        benchmark_name = input("Enter the name of the benchmark: ")
        if benchmark_name not in ["richards", "deltablue", "nbody", "fannkuch"]:
            print("Invalid benchmark name! Please choose 'richards', 'deltablue', 'fannkuch' or 'nbody'.")
        else:
            break

    while True:
        metric_name = input("Enter one of three metrics: tmax, tmin, orig: ")
        if metric_name not in ["tmax", "tmin", "orig"]:
            print("Invalid metric name! Please choose 'tmax', 'tmin', or 'orig'.")
        else:
            break

    while True:
        no_of_iterations = int(input("Enter the number of iterations between 1-25: "))
        no_of_iterations_list = list(range(1, 26))
        if no_of_iterations not in no_of_iterations_list:
            print("Invalid iteration count! Please choose a number between 1 and 25.")
        else:
            break

    final_itr_arg = 1
    if benchmark_name == "richards" or benchmark_name == "deltablue":
        final_itr_arg = 100
    elif benchmark_name == "fannkuch":
        final_itr_arg = 5
    else:
        final_itr_arg = ""


    t_max_commands = [
        "./python.exe -X jit -X jit-list-file=Tools/benchmarks/jitlist_{benchmark_name}_static.txt -X jit-enable-jit-list-wildcards -X jit-shadow-frame -X install-strict-loader Tools/benchmarks/{benchmark_name}_static.py {final_itr_arg}",
        "./python.exe -X jit -X jit-list-file=Tools/benchmarks/jitlist_{benchmark_name}_static.txt -X jit-enable-jit-list-wildcards -X install-strict-loader Tools/benchmarks/{benchmark_name}_static.py {final_itr_arg}",
        "./python.exe -X install-strict-loader Tools/benchmarks/{benchmark_name}_static.py {final_itr_arg}",
        "./python.exe -X jit -X jit-list-file=Tools/benchmarks/jitlist_{benchmark_name}_static.txt -X jit-enable-jit-list-wildcards -X jit-shadow-frame Tools/benchmarks/{benchmark_name}_static.py {final_itr_arg}",
        "./python.exe -X jit -X jit-list-file=Tools/benchmarks/jitlist_{benchmark_name}_static.txt -X jit-enable-jit-list-wildcards Tools/benchmarks/{benchmark_name}_static.py {final_itr_arg}",
        "./python.exe Tools/benchmarks/{benchmark_name}_static.py {final_itr_arg}"
    ]

    t_min_commands = [
        "./python.exe -X jit -X jit-list-file=Tools/benchmarks/jitlist_{benchmark_name}_static_basic.txt -X jit-enable-jit-list-wildcards -X jit-shadow-frame -X install-strict-loader Tools/benchmarks/{benchmark_name}_static_basic.py {final_itr_arg}",
        "./python.exe -X jit -X jit-list-file=Tools/benchmarks/jitlist_{benchmark_name}_static_basic.txt -X jit-enable-jit-list-wildcards -X install-strict-loader Tools/benchmarks/{benchmark_name}_static_basic.py {final_itr_arg}",
        "./python -X install-strict-loader Tools/benchmarks/{benchmark_name}_static_basic.py {final_itr_arg}"
        "./python.exe -X jit -X jit-list-file=Tools/benchmarks/jitlist_{benchmark_name}_static_basic.txt -X jit-enable-jit-list-wildcards -X jit-shadow-frame Tools/benchmarks/{benchmark_name}_static_basic.py {final_itr_arg}",
        "./python.exe -X jit -X jit-list-file=Tools/benchmarks/jitlist_{benchmark_name}_static_basic.txt -X jit-enable-jit-list-wildcards Tools/benchmarks/{benchmark_name}_static_basic.py {final_itr_arg}",
        "./python.exe Tools/benchmarks/{benchmark_name}_static_basic.py {final_itr_arg}"
    ]

    orig_commands = [
        "./python.exe -X jit -X jit-list-file=Tools/benchmarks/jitlist_main.txt -X jit-enable-jit-list-wildcards -X jit-shadow-frame Tools/benchmarks/{benchmark_name}.py {final_itr_arg}",
        "./python.exe -X jit -X jit-list-file=Tools/benchmarks/jitlist_main.txt -X jit-enable-jit-list-wildcards Tools/benchmarks/{benchmark_name}.py {final_itr_arg}",
        "./python.exe -X jit Tools/benchmarks/{benchmark_name}.py {final_itr_arg}",
    ]

    if metric_name == "tmax":
        commands = t_max_commands
        normalizer_metric = "T-Max"
    elif metric_name == "tmin":
        commands = t_min_commands
        normalizer_metric = "T-Min"
    else:
        commands = orig_commands
        normalizer_metric = "Orig"


    run_commands_and_record_runtimes(benchmark_name, commands, metric_name, no_of_iterations, final_itr_arg)

    print("We are normalizing the table by dividing every row by the first value in that row\n")
    normalize_option = input("Do you want to normalize the CSV file? (y/n): ").lower()
    if normalize_option == "y":
        csv_filename = os.path.join("benchmark_runtime_records", f"{benchmark_name}_{metric_name}_runtimes.csv")
        normalize_csv(csv_filename, normalizer_metric)
