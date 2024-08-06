#!/bin/bash
/usr/local/cuda/bin/nvcc -forward-unknown-to-host-compiler \
  -g -G -std=c++17 --generate-code=arch=compute_75,code=sm_75 \
  -Xcompiler=-fPIC -MD  \
  -x cu -c ./rdma_shim.cu \
  -o rdma_shim_cuda.cubin \
  --ptxas-options=-v \
  -cubin

 /usr/local/cuda/bin/nvdisasm -g -ndf rdma_shim_cuda.cubin > rdma_shim_cuda.cubin.txt
 /usr/local/cuda/bin/nvdisasm -gi -ndf rdma_shim_cuda.cubin > rdma_shim_cuda.cubin.gi.txt

