import csv
import os
f = []

d = "/Users/mgallagher/Downloads"

for (dirpath, dirnames, filenames) in os.walk(d):
    f.extend(filenames)
    break

top = []
for each in f:
    if len(each) == 45:
        top.append(each)

a = []
for each in top:
    with open(d+"/"+each) as f:
        a = a + [{k: str(v) for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]

print a[0]