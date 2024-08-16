import psutil
import time
import signal
import argparse
import numa
import sensors

# (C) 2024 Massimo Girondi massimo@girondi.net
# This script collects system statistics, and print them to stdout.
# These should be consumed by npf or stored in a file for later processing

loads=[]
percs=[]
def on_exit(sig, frame):
    #cores = psutil.cpu_count()
    #print("RESULT-CPU_PERC", sum(percs) / len(percs))
    #print("RESULT-CPU_LOAD", (sum(loads) / len(loads)))

    exit(0)



def parse_cores(cores):
    new_cores = []
    for c in cores.split(","):
        if "-" in c:
            start, stop = c.split("-")
            these = list(range(int(start), int(stop)+1))
            new_cores += these
        else:
            new_cores += [c]
    return new_cores



parser = argparse.ArgumentParser()
parser.add_argument("--interval", default=1, type=float)
parser.add_argument("--ncores", default=-1, type=int)
parser.add_argument("--numa", default=-1, type=int)
parser.add_argument("--cores", default="", type=str)
parser.add_argument("--name", default="", type=str)
parser.add_argument("--load", action="store_true")
parser.add_argument("--interrupts", action="store_true")
parser.add_argument("--power", action="store_true")

args = parser.parse_args()

if args.cores == "":
    if args.numa == -1:
        if args.ncores == -1:
            ncores = psutil.cpu_count()
        else:
            ncores = args.ncores
        cores = list(range(0, ncores))
    else:
        cores = numa.info.node_to_cpus(args.numa)
        if args.ncores != -1:
            cores = cores[:args.ncores]
else:
    cores = parse_cores(args.cores)

ncores = len(cores)
print("Collecting stats from cores", cores)

power_sensor = None
if args.power:
    sensors.init()
    try:
        for chip in sensors.iter_detected_chips():
            if "power" in str(chip):
                for feature in chip:
                    if power_sensor is None:
                        power_sensor = feature
                        print("Using",chip,"/", feature.label, "for power reporting")
                    else:
                        print("Also", feature, "may be suitable for power reporting, but we ignore it!")

        # print '%s at %s' % (chip, chip.adapter_name)
        # for feature in chip:
        #     print '  %s: %.2f' % (feature.label, feature.get_value())
    except:
        power_sensor = None


signal.signal(signal.SIGABRT, on_exit)
signal.signal(signal.SIGINT, on_exit)

last_stats = psutil.cpu_stats()
last_t = time.time()

while True:
    t = time.time()
    p = psutil.cpu_percent(args.interval,percpu=True)
    p = [pp for i,pp in enumerate(p) if i in cores]
    p_avg = sum(p) / ncores
    load1m, _, _ = psutil.getloadavg()

    #loads.append(load1m)
    #percs.append(p)
    name = "" if args.name== "" else f"_{args.name}"
    t = int(t*1000)
    print(f"{t}-RESULT-CPU_PERC{name} {p_avg}")
    print(f"{t}-RESULT-CPU_CORES{name} {p_avg*ncores/100}")
    if args.load:
        print(f"{t}-RESULT-LOAD1M{name} {load1m}")
    if power_sensor:
        print(f"{t}-RESULT-SYSPOWER {power_sensor.get_value()}")



    if args.interrupts:
        stats = psutil.cpu_stats()
        delta = (t - last_t) / 1000
        print(f"{t}-RESULT-INTERRUPTS{name} {(stats.interrupts - last_stats.interrupts) / delta}")
        print(f"{t}-RESULT-SOFT_INTERRUPTS{name} {(stats.soft_interrupts -last_stats.soft_interrupts) / delta}")
        last_t = t
        last_stats = stats
