# Get the source

_It should_ be enough to clone this repository recursively:
```
git clone https://github.com/rdma-from-gpu/rdma-from-gpu --recursive
```

However, you may want to manually `sync` or `update` individual submodules for the different parts of the project.

# Get rdma-core

For this, follow the upstream documentation for rdma-core.
But in general, `./build.sh` should do the job and get you a working library that can be used from our tools

# Compile rdma-shim

This is the layer that interposes between the standard-ish rdma-core and our apps.
You should be able to compile it with cmake:

```
cmake . -B build 
make -j -C build
```

There shouldn't be any hard dependency for this library, beside the CUDA compiler (and related libraries).

# Compile TVM


TVM follows standard TVM compilation.
To simplify your life, you can use `helpers/tvm_config.cmake` as a starting point, which should be fine for most cases.

```
cd tvm
mkdir build
cd build
cp ../../helpers/tvm_config.cmake config.cmake
cmake ..
make -j
```

# Compile apps

These requires some additional libraries, which are in general installed running `cd extern; ./build.sh`.

On top of these, you'll need CUDA libraries (yes, also for the client - to keep the project structure simpler), and Boost development packages from your distribution (e.g. `libboost-all-dev` on Ubuntu).

Once you have them, these should to the job and you should find binaries in the `build` folder ready to be tested:

```
cmake . -B build
make -j -C build
```

# Experiments

The folder `experiments` uses the compiled binaries on the steps above to retrieve results.
These are run via `ansible`, and `stdout` is collect from each run to extract the performance values.
