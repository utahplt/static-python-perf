import os
import statistics
from scipy import stats


# Execute Python file and collect its output as a list of runtimes.
def run_once(file_name):
    command = f"python3 {file_name}"
    stream = os.popen(command)
    output = stream.read()
    return float(output)


def run_many(file_name, num_iterations):
    return [run_once(file_name) for _ in range(num_iterations)]


""" Basically, this function checks for stability by generating runtime values by calling run many. Checks if confidence interval is within 10 percent of the sample mean"""


def check_stability(file_name, num_iterations, max_attempts=3):
    for attempt in range(max_attempts):
        runtimes = run_many(file_name, num_iterations)

        print(f"Attempt {attempt + 1}:")
        for i, runtime in enumerate(runtimes):
            print(f"Run {i + 1}: {runtime} seconds")

        mean_runtime = statistics.mean(runtimes)

        std_dev = statistics.stdev(runtimes)
        confidence_interval = stats.t.interval(0.95, len(runtimes) - 1, loc=mean_runtime,
                                               scale=std_dev / (len(runtimes) ** 0.5))

        """Stability check to see where the interval is within 10 percent of the sample mean"""
        lower_bound, upper_bound = confidence_interval
        acceptable_range = mean_runtime * 0.1

        if lower_bound <= mean_runtime - acceptable_range or upper_bound >= mean_runtime + acceptable_range:
            print("Unstable")
        else:
            print("Stable")

        # Print the mean and confidence interval
        print(f"Mean Runtime: {mean_runtime} seconds")
        print(f"Confidence Interval: {confidence_interval}")

        if attempt < max_attempts - 1 and (lower_bound <= mean_runtime - acceptable_range or upper_bound >= mean_runtime + acceptable_range):
            # If it's unstable and there are more attempts remaining, try again.
            print("Retrying")
        else:
            break


if __name__ == "__main__":
    file_name = "/Users/vivaan/PycharmProjects/Time-Track/static-python-perf/Benchmark/richards/untyped/main.py"
    num_iterations = 8
    max_attempts = 3  # Maximum number of attempts to stabilize
    check_stability(file_name, num_iterations, max_attempts)


###### Goals for this ########
# 1. call run many and check for stability by generating runtiem values by calling run many (confirm stability)
# 2. print out all the runtimes, and the average runtime
# all this stuff in a new function here
