import os
import statistics
from scipy import stats
import numpy as np
from scipy.stats import norm


def count_lines(file_name):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            return len(lines)
    except Exception as e:
        print(f"Error: Failed to read file {file_name}. {str(e)}")
        return None


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


# def check_stability(file_name, num_iterations, max_attempts=3):
#     def gen():
#         return run_many(file_name, num_iterations)
#
#     return driver(gen, bootstrap_confidence_interval, max_attempts)


def check_stability(file_name, num_iterations, max_attempts=3):
    def gen():
        return run_many(file_name, num_iterations)

    # Split the file path by '/'
    path_parts = file_name.split('/')

    # Join the path parts excluding the last one (file name) to get the directory path
    directory_path = '/'.join(path_parts[:-1])

    # Change the current working directory to the directory containing the Python file
    os.chdir(directory_path)

    # Get the number of lines in the file
    num_lines = count_lines(file_name)

    # return driver(gen, bootstrap_confidence_interval, max_attempts, num_lines)
    return driver(gen, bootstrap_confidence_interval, signed_rank_confidence_interval, max_attempts, num_lines)

# def driver(random_number_generator, ci_builder, max_iterations=20, num_lines=None):
#     data = random_number_generator()
#     data = [x for x in data if x is not None]  # Remove None values
#     if not data:
#         print("All iterations failed, cannot calculate confidence interval.")
#         return
#
#     old_data = data.copy()
#     converged = False
#     iteration = 1
#     while (not converged) and (iteration <= max_iterations):
#         conf_interval = ci_builder(data)
#         sample_mean = np.mean(data)
#         sample_mean_10_percent_interval = [sample_mean - 0.1 * sample_mean, sample_mean + 0.1 * sample_mean]
#         ci_within_10_percent_interval = (
#                 sample_mean_10_percent_interval[0] <= conf_interval[0]
#                 and sample_mean_10_percent_interval[1] >= conf_interval[1]
#         )
#         if ci_within_10_percent_interval:
#             converged = True
#         else:
#             iteration += 1
#             additional_data = random_number_generator()
#             additional_data = [x for x in additional_data if x is not None]  # Remove None values
#             old_data = np.concatenate((old_data, additional_data))
#             data = old_data
#
#     print(f"Iteration {iteration}:")
#     print("Sample:", data)
#     print("Confidence Interval:", conf_interval)
#     print("Sample Mean:", sample_mean)
#     print("10% Mean Interval:", sample_mean_10_percent_interval)
#     print("CI Interval within 10% Interval:", ci_within_10_percent_interval)
#
#     # Print the number of lines in the file
#     if num_lines is not None:
#         print(f"Number of Lines in the File: {num_lines}")
#
#     print("")

def driver(random_number_generator, bootstrap_ci_builder, signed_rank_ci_builder, max_iterations=20, num_lines=None):
    data = random_number_generator()
    data = [x for x in data if x is not None]  # Remove None values
    if not data:
        print("All iterations failed, cannot calculate confidence interval.")
        return

    old_data = data.copy()
    converged = False
    iteration = 1
    while (not converged) and (iteration <= max_iterations):
        bootstrap_conf_interval = bootstrap_ci_builder(data)
        signed_rank_conf_interval = signed_rank_ci_builder(data)

        sample_mean = np.mean(data)
        sample_mean_10_percent_interval = [sample_mean - 0.1 * sample_mean, sample_mean + 0.1 * sample_mean]

        # Check bootstrap confidence interval
        bootstrap_ci_within_10_percent_interval = (
                sample_mean_10_percent_interval[0] <= bootstrap_conf_interval[0]
                and sample_mean_10_percent_interval[1] >= bootstrap_conf_interval[1]
        )

        # Check signed rank confidence interval
        signed_rank_ci_within_10_percent_interval = (
                sample_mean_10_percent_interval[0] <= signed_rank_conf_interval[0]
                and sample_mean_10_percent_interval[1] >= signed_rank_conf_interval[1]
        )

        if bootstrap_ci_within_10_percent_interval or signed_rank_ci_within_10_percent_interval:
            converged = True
        else:
            iteration += 1
            additional_data = random_number_generator()
            additional_data = [x for x in additional_data if x is not None]  # Remove None values
            old_data = np.concatenate((old_data, additional_data))
            data = old_data

    print(f"Iteration {iteration}:")
    print("Sample:", data)
    print("Bootstrap Confidence Interval:", bootstrap_conf_interval)
    print("Signed Rank Confidence Interval:", signed_rank_conf_interval)
    print("Sample Mean:", sample_mean)
    print("10% Mean Interval:", sample_mean_10_percent_interval)
    print("Bootstrap CI Interval within 10% Interval:", bootstrap_ci_within_10_percent_interval)
    print("Signed Rank CI Interval within 10% Interval:", signed_rank_ci_within_10_percent_interval)

    # Print the number of lines in the file
    if num_lines is not None:
        print(f"Number of Lines in the File: {num_lines}")

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
    ranks = np.abs(np.arange(1, len(data) + 1))
    signed_ranks = np.where(data > np.median(data), ranks, -ranks)
    sample_mean = np.mean(data)

    sum_ranks = np.sum(np.abs(signed_ranks))

    # problem is maybe because of this
    se = np.sqrt((np.sum(signed_ranks ** 2) - len(data) * (len(data) + 1) ** 2 / 4) / (len(data) * (len(data) - 1)))

    z_alpha = norm.ppf(1 - alpha / 2)

    lower_bound = sample_mean - (z_alpha * se / np.sqrt(len(data)))
    upper_bound = sample_mean + (z_alpha * se / np.sqrt(len(data)))

    return lower_bound, upper_bound


if __name__ == "__main__":
    file_paths = [
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/call_method/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/call_method_slots/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/call_simple/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/chaos/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/deltablue/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/espionage/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/evolution/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/fannkuch/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/float/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/futen/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/go/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/http2/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/meteor/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/nbody/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/nqueens/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/pidigits/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/pystone/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/pythonflow/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/richards/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/sample_fsm/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/slowsha/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/spectralnorm/untyped/main.py",
        # # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/stats/untyped/main.py", path problem
        "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/take5/untyped/main.py",
    ]
    num_iterations = 8
    max_attempts = 3

    for file_path in file_paths:
        print(f"Running benchmark: {file_path}")
        check_stability(file_path, num_iterations, max_attempts)
