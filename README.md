This is the public code release for our paper "Toward GPU-centric Networking on Commodity Hardware".




# Cite us

@inproceedings{10.1145/3642968.3654820,
author = {Girondi, Massimo and Scazzariello, Mariano and Maguire, Gerald Q. and Kosti\'{c}, Dejan},
title = {Toward GPU-centric Networking on Commodity Hardware},
year = {2024},
isbn = {9798400705397},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3642968.3654820},
doi = {10.1145/3642968.3654820},
abstract = {GPUs are emerging as the most popular accelerator for many applications, powering the core of machine learning applications. In networked GPU-accelerated applications input \& output data typically traverse the CPU and the OS network stack multiple times, getting copied across the system's main memory. These transfers increase application latency and require expensive CPU cycles, reducing the system's efficiency, and increasing the overall response times. These inefficiencies become of greater importance in latency-bounded deployments, or with high throughput, where copy times could quickly inflate the response time of modern GPUs. We leverage the efficiency and kernel-bypass benefits of RDMA to transfer data in and out of GPUs without using any CPU cycles or synchronization. We demonstrate the ability of modern GPUs to saturate a 100-Gbps link, and evaluate the network processing time in the context of an inference serving application.},
booktitle = {Proceedings of the 7th International Workshop on Edge Systems, Analytics and Networking},
pages = {43–48},
numpages = {6},
keywords = {Commodity Hardware, GPUs, Inference Serving, RDMA},
location = {Athens, Greece},
series = {EdgeSys '24}
}



# License
The code in this repository, unless otherwise stated, is released under the GNU GPL v3 license. See [LICENSE](LICENSE).
