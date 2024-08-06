#!/usr/bin/python3
import re
import sys
import psutil



def pidof(pgname):
    pids = []
    for proc in psutil.process_iter(['name', 'cmdline']):
        # search for matches in the process name and cmdline
        if proc.info['name'] == pgname or \
                proc.info['cmdline'] and proc.info['cmdline'][0] == pgname:
            pids.append(str(proc.pid))
    return pids



name =sys.argv[1]
pid = int(pidof(name)[0])
address = int(sys.argv[2], 16)

pattern = re.compile("([0-9a-fx]+)-([0-9a-fx]+)(.* )+(.+)$")
with open(f"/proc/{pid}/maps") as f:
    for line in f:
        s = pattern.search(line)
        start = int(f"0x{s.group(1)}",16)
        stop = int(f"0x{s.group(2)}",16)
        n = len(s.groups())
        name =  s.group(n)
        #print(start, stop, name)
        if start <= address  <= stop:
            print(line)
