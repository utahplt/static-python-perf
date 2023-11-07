import os
import statistics
from scipy import stats
import numpy as np


# Execute Python file and collect its output as a list of runtimes.
def run_once(file_name):
    try:
        command = f"python3 {file_name}"
        stream = os.popen(command)
        output = stream.read()
        return float(output)
    except ValueError:
        print(f"Error: Failed to convert output to float for {file_name}")
        return None


def run_many(file_name, num_iterations):
    return [run_once(file_name) for _ in range(num_iterations)]


def check_stability(file_name, num_iterations, max_attempts=3):
    def gen():
        return run_many(file_name, num_iterations)

    return driver(gen, bootstrap_confidence_interval, max_attempts)


def driver(random_number_generator, ci_builder, max_iterations=20):
    data = random_number_generator()
    data = [x for x in data if x is not None]  # Remove None values
    if not data:
        print("All iterations failed, cannot calculate confidence interval.")
        return

    old_data = data.copy()
    converged = False
    iteration = 1
    while (not converged) and (iteration <= max_iterations):
        conf_interval = ci_builder(data)
        sample_mean = np.mean(data)
        sample_mean_10_percent_interval = [sample_mean - 0.1 * sample_mean, sample_mean + 0.1 * sample_mean]
        ci_within_10_percent_interval = (
                sample_mean_10_percent_interval[0] <= conf_interval[0]
                and sample_mean_10_percent_interval[1] >= conf_interval[1]
        )
        if ci_within_10_percent_interval:
            converged = True
        else:
            iteration += 1
            additional_data = random_number_generator()
            additional_data = [x for x in additional_data if x is not None]  # Remove None values
            old_data = np.concatenate((old_data, additional_data))
            data = old_data

    print(f"Iteration {iteration}:")
    print("Sample:", data)
    print("Confidence Interval:", conf_interval)
    print("Sample Mean:", sample_mean)
    print("10% Mean Interval:", sample_mean_10_percent_interval)
    print("CI Interval within 10% Interval:", ci_within_10_percent_interval)
    print("")


def bootstrap_confidence_interval(data, alpha=0.05, num_resamples=10000):
    resamples = np.random.choice(data, size=(num_resamples, len(data)), replace=True)
    sample_means = np.mean(resamples, axis=1)
    lower_percentile = (1 - alpha) / 2
    upper_percentile = 1 - lower_percentile
    lower_bound = np.percentile(sample_means, lower_percentile * 100)
    upper_bound = np.percentile(sample_means, upper_percentile * 100)
    return lower_bound, upper_bound


def signed_rank_confidence_interval(data, alpha=0.05):
    data = np.sort(data)
    ranks = np.arange(1, len(data) + 1)
    signed_ranks = np.where(data > np.median(data), ranks, -ranks)
    sample_mean = np.mean(data)
    sum_ranks = np.sum(signed_ranks)
    se = np.sqrt((len(data) * (len(data) + 1) * (2 * len(data) + 1)) / 6)
    z_alpha = np.abs(np.percentile(np.random.normal(0, 1, 10000), (1 - alpha / 2) * 100))
    lower_bound = sample_mean - (z_alpha * se / np.sqrt(24))
    upper_bound = sample_mean + (z_alpha * se / np.sqrt(24))
    return lower_bound, upper_bound


if __name__ == "__main__":
    file_paths = [
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/call_method/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/call_method_slots/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/call_simple/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/chaos/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/deltablue/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/espionage/untyped/main.py",
        # help with evolution
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/fannkuch/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/float/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/futen/untyped/main.py", error here, datafile import error
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/go/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/http2/untyped/main.py", error here, datafile import error
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/meteor/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/nbody/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/nqueens/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/pidigits/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/pystone/untyped/main.py",
        # pythonflow has same file thing
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/richards/untyped/main.py",
        # sample_fsm file thing
        # same with slowsha
        # where is the function call for spectralnorm?
        # how should i approach stats
        # take5 problem
    ]
    num_iterations = 8
    max_attempts = 3

    for file_path in file_paths:
        print(f"Running benchmark: {file_path}")
        check_stability(file_path, num_iterations, max_attempts)
