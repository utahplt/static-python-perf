import pstats
import os
import io
import json


data = {} # {filename: time}

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
        
        # only retain lines with site-packages/django
        lines = filter(lambda x: "site-packages/django" in x, lines)
        
        # for each line, extract the filename (element 5) and time (element 1)
        for line in lines:
            line = line.split()
            filename = line[5].split("site-packages/django/", 2)[1].split(":")[0]
            time = float(line[1])
            if filename in data:
                data[filename] += time
            else:
                data[filename] = time

# sort the data by time
data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))

with open("django_prof_report.json", "w") as f:
    f.write(json.dumps(data, indent=4))
