import os
import numpy as np
from scipy.stats import norm
from prettytable import PrettyTable


def count_lines(file_name):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            return len(lines)
    except Exception as e:
        print(f"Error: Failed to read file {file_name}. {str(e)}")
        return None


def run_once(file_name):
    try:
        command = f"python3 {file_name}"
        stream = os.popen(command)
        output = stream.read().strip()
        return float(output) if output else 0.0

    #    output = stream.read()
    #     return float(output)
    # except ValueError:
    #     print(f"Error: Failed to convert output to float for {file_name}")

    except ValueError as ve:
        print(f"Error: Failed to convert output to float for {file_name}. Error: {ve}")
        return None
    except Exception as e:
        print(f"Error: An unexpected error occurred while running {file_name}. {str(e)}")
        return None


def run_many(file_name, num_iterations):
    return [run_once(file_name) for _ in range(num_iterations)]


def check_stability(file_name, num_iterations, max_attempts=3):
    def gen():
        return run_many(file_name, num_iterations)

    path_parts = file_name.split('/')
    directory_path = '/'.join(path_parts[:-1])
    os.chdir(directory_path)

    num_lines = count_lines(file_name)

    return driver(gen, bootstrap_confidence_interval, signed_rank_confidence_interval, max_attempts, num_lines)


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

    # Create a PrettyTable for better output formatting
    table = PrettyTable()
    table.field_names = ["Metric", "Value"]
    table.add_row(["Iteration", iteration])
    table.add_row(["Sample", data])
    table.add_row(["Bootstrap Confidence Interval", bootstrap_conf_interval])
    table.add_row(["Signed Rank Confidence Interval", signed_rank_conf_interval])
    table.add_row(["Sample Mean", sample_mean])
    table.add_row(["10% Mean Interval", sample_mean_10_percent_interval])
    table.add_row(["Bootstrap CI Interval within 10% Interval", bootstrap_ci_within_10_percent_interval])
    table.add_row(["Signed Rank CI Interval within 10% Interval", signed_rank_ci_within_10_percent_interval])

    # Print the number of lines in the file
    if num_lines is not None:
        table.add_row(["Number of Lines in the File", num_lines])

    print(table)
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
        ### Untyped Files ###
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
        "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/slowsha/untyped/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/spectralnorm/untyped/main.py",
        # # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/stats/untyped/main.py", path problem
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/take5/untyped/main.py",
    ]

    static_files = [
        ### Shallow Files ####

        "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/call_method/shallow/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/call_method_slots/shallow/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/call_simple/shallow/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/chaos/shallow/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/deltablue/shallow/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/espionage/shallow/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/evolution/shallow/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/fannkuch/shallow/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/float/shallow/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/futen/shallow/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/go/shallow/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/http2/shallow/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/meteor/shallow/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/nbody/shallow/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/nqueens/shallow/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/pidigits/shallow/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/pystone/shallow/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/pythonflow/shallow/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/richards/shallow/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/sample_fsm/shallow/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/slowsha/shallow/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/spectralnorm/shallow/main.py",
        # # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/stats/shallow/main.py", path problem
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/take5/shallow/main.py",

        ### advanced files ### !! Some don't work due to lack of advanced files.

        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/call_method/advanced/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/call_method_slots/advanced/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/call_simple/advanced/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/chaos/advanced/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/deltablue/advanced/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/espionage/advanced/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/evolution/advanced/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/fannkuch/advanced/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/float/advanced/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/futen/advanced/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/go/advanced/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/http2/advanced/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/meteor/advanced/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/nbody/advanced/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/nqueens/advanced/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/pidigits/advanced/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/pystone/advanced/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/pythonflow/advanced/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/richards/advanced/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/sample_fsm/advanced/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/slowsha/advanced/main.py",
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/spectralnorm/advanced/main.py",
        # # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/stats/advanced/main.py", path problem
        # "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/take5/advanced/main.py",

    ]

    num_iterations = 8
    max_attempts = 3

    for file_path in file_paths:
        print(f"Running benchmarks in directory: {file_path}")
        # Get the directory path from the file_path
        directory_path = '/'.join(file_path.split('/')[:-1])
        for file_name in os.listdir(directory_path):
            if file_name.endswith(".py"):
                full_file_path = os.path.join(directory_path, file_name)
                print(f"  Running benchmark: {full_file_path}")
                check_stability(full_file_path, num_iterations, max_attempts)

    # print("\nNumber of lines in the files:")
    # table_lines = PrettyTable()
    # table_lines.field_names = ["File", "Number of Lines"]
    #
    # for static_file in static_files:
    #     num_lines = count_lines(static_file)
    #     table_lines.add_row([static_file, num_lines])
    #
    # print(table_lines)


    print("Line Count Calculator")

    print("\nNumber of lines in the files:")
    table_lines = PrettyTable()
    table_lines.field_names = ["File", "Number of Lines"]

    for file_path in file_paths:
        # print(f"Running benchmarks in directory: {file_path}")
        directory_path = '/'.join(file_path.split('/')[:-1])

        # Iterate over all .py files in the directory
        for file_name in os.listdir(directory_path):
            if file_name.endswith(".py"):
                full_file_path = os.path.join(directory_path, file_name)
                # print(f"  Running benchmark: {full_file_path}")

                # Get the number of lines for the file
                num_lines = count_lines(full_file_path)

                # Add to the table
                table_lines.add_row([full_file_path, num_lines])

    print(table_lines)

"""
1. Run 3 for each benchmark: Untyped, Shallow, advanced; essentially running the main file for all 3
2. figure out how we can implement a randomized type system for all the code
3. make a plan!


"""