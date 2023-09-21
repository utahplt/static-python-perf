import sys
import os


# Execute Python file and collect it's output as a string.
def run_once(file_name):
    command = f"python3 {file_name}"
    stream = os.popen(command)
    output = stream.read()
    return float(output)

# 1. call run many and check for stability by generating runtiem values by calling run many (confirm stability)
# 2. print out all the runtimes, and the average runtime
# all this stuff in a new function here

def run_many(file_name, num_iterations):
    return[run_once(file_name) for i in range(num_iterations)]







if __name__ == "__main__":
    # num_iterations = 8
    #
    # total_runtime = 0
    #
    # for i in range(num_iterations):
    #
    #     if not success:
    #         print("Benchmark failed")
    #         sys.exit(1)
    #
    #     total_runtime += runtime
    #
    # average_runtime = total_runtime / num_iterations
    # print(f"Average Runtime over {num_iterations} iterations = {average_runtime} seconds")

    runtime = run_once("/Users/Vivaan/Desktop/Static\\ Python/static-python-perf/Benchmark/richards/untyped/main.py")
    print(runtime + 1)
