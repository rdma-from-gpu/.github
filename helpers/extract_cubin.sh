#!/bin/bash
CUDA_BIN=/usr/local/cuda/bin
export PATH=$CUDA_BIN:$PATH

mkdir build/cubins
cd build/cubins
#cuobjdump build/rdma_from_gpu --list-elf
cuobjdump ../librdma_shim_cuda.a --list-elf
cuobjdump ../librdma_shim_cuda.a --extract-elf all
nvdisasm ./librdma_shim_cuda.1.sm_75.cubin
nvdisasm -cfg ./librdma_shim_cuda.1.sm_75.cubin | dot -ocfg.png -Tpng
nvdisasm -bbcfg ./librdma_shim_cuda.1.sm_75.cubin | dot -obbcfg.png -Tpng
nvdisasm -g ./librdma_shim_cuda.1.sm_75.cubin > annotated.txt

