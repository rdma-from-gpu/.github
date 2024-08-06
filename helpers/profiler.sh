#!/bin/bash
#mkdir build_nvtx
#CUDA_PATH=/usr/local/cuda cmake . -DCMAKE_CUDA_ARCHITECTURES=75 -B build_nvtx -DCMAKE_BUILD_TYPE=Release -DCUDA_TRACING=1
#make -j -C build_nvtx VERBOSE=1 rdma_from_gpu

sudo /usr/local/cuda-12.0/bin/nsys profile \
  --output=/tmp/rdma_from_gpu.nsys-rep --force-overwrite=true \
  ./build_nvtx/rdma_from_gpu 

#sudo /usr/local/cuda-12.0/bin/nsys analyze\
#  /tmp/rdma_from_gpu.nsys-rep 
sudo /usr/local/cuda-12.0/bin/nsys stats  \
  /tmp/rdma_from_gpu.nsys-rep \
  --format json --report gpukernsum \
  --output /tmp/rdma_from_gpu

python3 gputrace_to_npf.py /tmp/rdma_from_gpu_gpukernsum.json

