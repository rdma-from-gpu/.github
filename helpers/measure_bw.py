#!/usr/bin/python3

# (C) 2024 Massimo Girondi massimo@girondi.net GNU GPL v3
# This script retrieve a packet counter from an OpenFlow controller
# And prints the average bandwidth passing through that port.
# If "read" is given, it would just plot the counters previously retrieved and saved


import requests
import argparse
import time
import json
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import signal
import datetime as dt
session = None
counters = []
args = None
def get_counters(url, port, interval):
    global session
    while True:
        if session is None:
            session = requests.Session()
        j = session.get(url+str(port)).text
        yield json.loads(j)
        time.sleep(interval)

def get_filename():
    global filename
    global args
    t = dt.datetime.now().isoformat()
    name = str(args.port) if args.name == "" else args.name
    if args.outdir is not None:
        filename=args.outdir+"/bw_"+ name
    else:
        filename = f"bw_{name}_{t}"
    return filename

def format_bw(bw):
    if bw > 1e9:
        bw = f"{bw/1e9} Gbps"
    elif bw > 1e6:
        bw = f"{bw/1e6} Mbps"
    elif bw > 10e3:
        bw = f"{bw/1e3} Kbps"
    else: 
        bw = f"{bw} bps"
    return bw
def print_bw(data):
    print(f"TX: {format_bw(data['tx_bps'])}, RX: {format_bw(data['rx_bps'])}", data)
def retrieve_data(url="http://192.168.3.1:7777/port_stats?port=", port=29, interval=1, callback=print_bw):
    global counters
    last = None
    for c in get_counters(url, port, interval):
        # Ideally, time should be supplied by the controller
        if not "time" in c:
            t = time.time()
            c["time"] = t
        if last is not None:
            t = c["t"]-last["t"]
            if t:
                c["rx_bps"] = 8*(c["rx_bytes"] - last["rx_bytes"]) / t
                c["tx_bps"] = 8*(c["tx_bytes"] - last["tx_bytes"]) / t
                callback(c)
                counters.append(c)
        last = c

def update(data):
    global args
    if (args.npf):
        if args.epoch:
            #t = int(dt.datetime.now().timestamp()*1e9)
            t = int(dt.datetime.now().timestamp()) # We are fine with seconds precision
            print(f"{t}-RESULT-RX_BPS_{args.name} {data['rx_bps']}")
            print(f"{t}-RESULT-TX_BPS_{args.name} {data['tx_bps']}")
        else:
            t = (dt.datetime.now() - start).total_seconds()
            print(f"BW-{t}-RESULT-RX_BPS_{args.name} {data['rx_bps']}")
            print(f"BW-{t}-RESULT-TX_BPS_{args.name} {data['tx_bps']}")
    else:
        print_bw(data)



def save_csv(filename):
    global counters
    first = counters[0]
    print("Saving counters to", filename)
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = first.keys())
        writer.writeheader()
        writer.writerows(counters)
    return filename

def save_plot(filename = None):
    global counters
    global args
    rx = [c["rx_bps"] for c in counters]
    tx = [c["tx_bps"] for c in counters]
    times = [c["time"] for c in counters]
    times = [t - times[0] for t in times]
    fig, ax = plt.subplots()
    ax.plot(times, rx, label="RX")
    ax.plot(times, tx, label="TX")
    fig.legend()
    ax.set_xlabel("Time")
    ax.set_ylabel("BW")
    bps_formatter = matplotlib.ticker.EngFormatter(unit='bps')
    ax.yaxis.set_major_formatter(bps_formatter)
    plt.title("BW stats for port "+str(args.port)+ " ["+args.name+"]")
    print("Saving plot to", filename)
    fig.savefig(filename)

def on_exit(signal, frame):
    global counters
    first = counters[0]
    last = counters[-1]
    t = last["time"] - first["time"]

    print(f"RESULT-RX_BYTES_{args.name} {last['rx_bytes'] - first['rx_bytes']}")
    print(f"RESULT-TX_BYTES_{args.name} {last['tx_bytes'] - first['tx_bytes']}")
    print(f"RESULT-RX_AVG_{args.name} {(last['rx_bytes'] - first['rx_bytes'])*8.0 / t}")
    print(f"RESULT-TX_AVG_{args.name} {(last['tx_bytes'] - first['tx_bytes'])*8.0 / t}")
    if args.read is None:
        t = dt.datetime.now().isoformat()
        filename = f"bw_{t}"
        save_csv(get_filename()+".csv")
        save_plot(get_filename()+".pdf")
    exit(0)

if __name__ == "__main__":

    start = dt.datetime.now()
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://192.168.3.1:7777/port_stats?port=")
    parser.add_argument("--port", default="29", type=int)
    parser.add_argument("--interval", default=1, type=float)
    parser.add_argument("--read", default=None, type=str)
    parser.add_argument("--outdir", default=None, type=str)
    parser.add_argument("--name", default="", type=str)
    parser.add_argument("--npf", action="store_true")
    parser.add_argument("--epoch", action="store_true", help="Print epoch in ns, without BW- prefix")
    args = parser.parse_args()

    if args.read != None:
        with open(args.read, 'r') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            for c in reader:
                cc={k:float(v) for k,v in zip(header,c)}
                counters.append(cc)

            filename = ".".join(args.read.split(".")[:-1])
            save_plot(filename + ".pdf")
    else:
        signal.signal(signal.SIGINT, on_exit)
        retrieve_data(args.url, args.port, args.interval, update)

