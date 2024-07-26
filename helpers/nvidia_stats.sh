#!/bin/bash

# (C) 2024 Massimo Girondi massimo@girondi.net
# This script collects statistcs from nvidia-smi and print them to stdout.
# These should be consumed by npf or stored in a file for later processing

CUDA_DEVICE=${CUDA_DEVICE:-0}
STATS_INTERVAL=${CUDA_STATS_INTERVAL:-1}

START=$(date +%s.%3N)
while true; do
	nvidia-smi  --query-gpu=memory.used,utilization.gpu,utilization.memory,power.draw --format=csv,nounits,noheader --id ${CUDA_DEVICE} > /tmp/nvidia_smi.txt
  #NOW=$(echo "$(date +%s.%3N) - ${START}" | bc -l)
  NOW=$(echo "$(date +%s%3N)")
	echo "${NOW}-RESULT-GPUMEM " $(cut -d, -f1 /tmp/nvidia_smi.txt)
	echo ${NOW}"-RESULT-GPUMEMPERC " $(cut -d, -f3 /tmp/nvidia_smi.txt)
	echo ${NOW}"-RESULT-GPUPERC " $(cut -d, -f2 /tmp/nvidia_smi.txt)
	echo ${NOW}"-RESULT-GPUPOWER " $(cut -d, -f4 /tmp/nvidia_smi.txt)
  sleep $STATS_INTERVAL
done

