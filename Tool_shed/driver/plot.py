from matplotlib import pyplot as plt
import numpy as np
import json
import argparse
import os

script_path = os.path.dirname(os.path.realpath(__file__))


def plot(benchmark):
    with open(f'{script_path}/results/{benchmark}.jsonl', 'r') as f:
        results = [json.loads(line) for line in f] # each line is {"ratios": {"untyped": ..., "shallow": ..., "advanced": ...}, "time": ...}
        
    # plot ratio untyped vs time
    for typing in ["untyped", "shallow", "advanced"]:
        untyped_ratios = [result["ratios"][typing] for result in results]
        times = [result["time"] for result in results]
        plt.scatter(untyped_ratios, times)
        plt.xlabel(f"Ratio of {typing} code")
        plt.ylabel("Time (s)")
        plt.title(f"{benchmark} - {typing} ratio vs time")
        
        # save the plot
        plt.savefig(f'{script_path}/results/{benchmark}_{typing}_ratio_vs_time.png')
        
        # clear the plot
        plt.clf()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('benchmark', type=str, help='Benchmark to run')
    args = parser.parse_args()
    benchmark = args.benchmark
    
    plot(benchmark)
