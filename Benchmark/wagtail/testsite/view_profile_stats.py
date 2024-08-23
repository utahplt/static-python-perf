import pstats
import os
import io

with open("prof_report.txt", "w") as f:
    f.write("   ncalls  tottime  percall  cumtime  percall filename:lineno(function)\n")

# loop through all files in 'profile_data' directory
for file in os.listdir("profile_data"):
    if file.endswith(".prof"):
        # print the file name
        print(file)
        buf = io.StringIO()
        # create a new instance of the Stats class
        s = pstats.Stats("profile_data/" + file, stream=buf)
        # sort the stats by time and print all but first 8 lines
        s.sort_stats("time").print_stats(20)

        lines = buf.getvalue().split("\n")[8:]

        with open("prof_report.txt", "a") as f:
            f.write("\n".join(lines) + "\n")
