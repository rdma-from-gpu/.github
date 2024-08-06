import json
import sys

with open(sys.argv[1]) as f:
    data = json.load(f)
for d in data:
    name = d["Name"]
    name = name.split("(")[0]
    avg = d["Avg (ns)"]
    n = d["Instances"]
    share = d["Time (%)"]
    print(f"RESULT-TRACE_AVG-{name} {avg}")
    print(f"RESULT-TRACE_N-{name} {n}")
    print(f"RESULT-TRACE_TIME_SHARE-{name} {share}")
