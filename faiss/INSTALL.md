
[TOC]

# 介绍

FAISS 是 Facebook AI 研究团队开源的针对聚类和相似性搜索库，它包含一种在任意大小的向量集合中搜索直到可能不适合在 RAM 中的新算法。它还包含用于评估和参数调整的支持代码。由于公司服务器没有连接外网，无法使用conda安装，所以直接源码安装，githup网站下载地址：

https://github.com/facebookresearch/faiss

安装方法参考安装说明：

https://github.com/facebookresearch/faiss/blob/master/INSTALL.md

faiss安装可以使用make工具或者cmake工具。make可以生成c++接口和python接口， cmake编译只能生成c++接口

# install

## Aanconda install

```bash
conda install mkl
conda install numpy

# CPU version only
conda install faiss-cpu -c pytorch
# Make sure you have CUDA installed before installing faiss-gpu, otherwise it falls back to CPU version
conda install faiss-gpu -c pytorch# [DEFAULT]For CUDA8.0, comes with cudatoolkit8.0
# pip install faiss-cpu
pip install faiss-cpu==1.6.0
```

## CPU make install
```bash
# env
# lspci | grep VGA
00:02.0 VGA compatible controller: Cirrus Logic GD 5446

# 查看机器型号
lsb_release -a

# 查看CPU是否支持avx2
grep avx /proc/cpuinfo
grep avx2 /proc/cpuinfo

# cat /proc/cpuinfo

# git clone
git fetch && git fetch --tags
git clone https://github.com/facebookresearch/faiss.git
git tag -l
git checkout tags/<tag_name>
git checkout tags/<tag_name> -b <branch_name>

# 安装swig-3.0.12
./configure --prefix=/home/yunwei/app/faiss/lib/swig --with-python3=/home/yunwei/app/anaconda3/bin/python

# 机器1
export LD_LIBRARY_PATH=/home/yunwei/app/mkl_linux
./configure --prefix=/home/yunwei/app/faiss/faiss_install --without-cuda --with-python=/home/yunwei/app/anaconda3/bin/python LDFLAGS=-L/home/yunwei/app/anaconda3/lib --with-swig=/home/yunwei/app/faiss/lib/swig/bin/swig

PYTHONCFLAGS = -I/home/yunwei/app/anaconda3/include -I/home/yunwei/app/anaconda3/lib/python3.7/site-packages/numpy/core/include/
PYTHONLIB    = -lpython
PYTHON = /home/yunwei/app/anaconda3/bin/python

# 机器2
./configure --prefix=/opt/software/faiss/lib/faiss --without-cuda --with-python=/opt/.pyenv/versions/3.6.3/envs/faiss-env-3.6.3/bin/python LDFLAGS=-L/opt/.pyenv/versions/3.6.3/envs/faiss-env-3.6.3/lib --with-swig=/opt/software/faiss/lib/swig/bin/swig

PYTHONCFLAGS = -I/opt/.pyenv/versions/3.6.3/include/python3.6m -I/opt/.pyenv/versions/3.6.3/envs/faiss-env-3.6.3/lib/python3.6/site-packages/numpy/core/include/
PYTHONLIB    = -lpython
PYTHON = /opt/.pyenv/versions/3.6.3/envs/faiss-env-3.6.3/bin/python

```

## GPU make install
```bash
./configure --prefix=/opt/software/faiss/lib/faiss-gpu-1 --with-python=/opt/.pyenv/versions/3.6.3/envs/faiss-gpu-3.6.3/bin/python LDFLAGS=-L/opt/share/lib64/mkl_linux/lib --with-swig=/opt/software/faiss/lib/swig/bin/swig --with-cuda=/usr/local/cuda-9.0

PYTHONCFLAGS = -I/opt/.pyenv/versions/3.6.3/include/python3.6m -I/opt/.pyenv/versions/3.6.3/envs/faiss-gpu-3.6.3/lib/python3.6/site-packages/numpy/core/include/
PYTHONLIB    = -lpython
PYTHON = /opt/.pyenv/versions/3.6.3/envs/faiss-gpu-3.6.3/bin/python

```


# 问题
## 问题1----需要配置LD_LIBRARY_PATH

```bash
export MKLROOT=/opt/.pyenv/versions/faiss-env-3.6.3/lib
export LD_PRELOAD=$MKLROOT/lib/intel64/libmkl_core.so:$MKLROOT/lib/intel64/libmkl_sequential.so
export LD_LIBRARY_PATH=/opt/share/lib64/mkl_linux:$LD_LIBRARY_PATH
export LD_PRELOAD=/opt/share/lib64/mkl_linux/libmkl_core.so:/opt/share/lib64/mkl_linux/libmkl_sequential.so

Traceback (most recent call last):
  File "/opt/.pyenv/versions/faiss-env-3.6.3/lib/python3.6/site-packages/faiss-1.6.0-py3.6.egg/faiss/__init__.py", line 39, in <module>
    from .swigfaiss_avx2 import *
ModuleNotFoundError: No module named 'faiss.swigfaiss_avx2'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/opt/.pyenv/versions/faiss-env-3.6.3/lib/python3.6/site-packages/faiss-1.6.0-py3.6.egg/faiss/swigfaiss.py", line 14, in swig_import_helper
    return importlib.import_module(mname)
  File "/opt/.pyenv/versions/3.6.3/lib/python3.6/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 994, in _gcd_import
  File "<frozen importlib._bootstrap>", line 971, in _find_and_load
  File "<frozen importlib._bootstrap>", line 955, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 658, in _load_unlocked
  File "<frozen importlib._bootstrap>", line 571, in module_from_spec
  File "<frozen importlib._bootstrap_external>", line 922, in create_module
  File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
ImportError: libmkl_intel_lp64.so: cannot open shared object file: No such file or directory

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/opt/.pyenv/versions/faiss-env-3.6.3/lib/python3.6/site-packages/faiss-1.6.0-py3.6.egg/faiss/__init__.py", line 47, in <module>
    from .swigfaiss import *
  File "/opt/.pyenv/versions/faiss-env-3.6.3/lib/python3.6/site-packages/faiss-1.6.0-py3.6.egg/faiss/swigfaiss.py", line 17, in <module>
    _swigfaiss = swig_import_helper()
  File "/opt/.pyenv/versions/faiss-env-3.6.3/lib/python3.6/site-packages/faiss-1.6.0-py3.6.egg/faiss/swigfaiss.py", line 16, in swig_import_helper
    return importlib.import_module('_swigfaiss')
  File "/opt/.pyenv/versions/3.6.3/lib/python3.6/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
ModuleNotFoundError: No module named '_swigfaiss'
>>> quit()
(faiss-env-3.6.3) [hotel-revenue-online@xhy-30-111-42 ~]$ echo $LD_LIBRARY_PATH
/opt/.pyenv/versions/faiss-env-3.6.3/lib/lib/intel64
(faiss-env-3.6.3) [hotel-revenue-online@xhy-30-111-42 ~]$ ll /opt/.pyenv/versions/faiss-env-3.6.3/lib/lib/intel64
ls: cannot access /opt/.pyenv/versions/faiss-env-3.6.3/lib/lib/intel64: No such file or directory
(faiss-env-3.6.3) [hotel-revenue-online@xhy-30-111-42 ~]$ ll /opt/.pyenv/versions/faiss-env-3.6.3/lib/lib/intel64
ls: cannot access /opt/.pyenv/versions/faiss-env-3.6.3/lib/lib/intel64: No such file or directory
```

## 问题2 -- 编译demos报错

```bash
在 demos/demo_sift1M.cpp 中增加头文件 #include <faiss/index_factory.h>

<command-line>:0:0: warning: "FINTEGER" redefined [enabled by default]
<command-line>:0:0: note: this is the location of the previous definition
demo_sift1M.cpp: In function ‘int main()’:
demo_sift1M.cpp:114:17: error: ‘index_factory’ is not a member of ‘faiss’
         index = faiss::index_factory(d, index_key);
                 ^
In file included from /usr/include/c++/4.8.2/cassert:43:0,
                 from demo_sift1M.cpp:13:
demo_sift1M.cpp:205:38: warning: comparison of unsigned expression >= 0 is always true [-Wtype-limits]
         assert (selected_params.size() >= 0 ||
```


## 问题3 -- 编译GPU test

```bash
./gpu/test/demo_ivfpq_indexing_gpu.cpp 增加头文件 #include <faiss/gpu/GpuCloner.h>

make -C gpu/test demo_ivfpq_indexing_gpu

make: Entering directory `/opt/software/faiss/faiss/gpu/test'
g++ -std=c++11 -DFINTEGER=int  -fopenmp -I/usr/local/cuda-9.0/include -I/opt/software/faiss/faiss -DFINTEGER=long -fPIC -m64 -Wno-sign-compare -g -O3 -Wall -Wextra -mpopcnt -msse4 -o demo_ivfpq_indexing_gpu.o -c demo_ivfpq_indexing_gpu.cpp
<command-line>:0:0: warning: "FINTEGER" redefined [enabled by default]
<command-line>:0:0: note: this is the location of the previous definition
demo_ivfpq_indexing_gpu.cpp: In function ‘int main()’:
demo_ivfpq_indexing_gpu.cpp:88:36: error: ‘index_gpu_to_cpu’ is not a member of ‘faiss::gpu’
         faiss::Index * cpu_index = faiss::gpu::index_gpu_to_cpu (&index);
                                    ^
make: *** [demo_ivfpq_indexing_gpu.o] Error 1
make: Leaving directory `/opt/software/faiss/faiss/gpu/test'
```

## 问题4 -- gpu/test/demo_ivfpq_indexing_gpu 执行异常
```bash



(faiss-gpu-3.6.3) [hotel-revenue-online@xhy-30-111-42 faiss]$ ./gpu/test/demo_ivfpq_indexing_gpu
[2.802 s] Generating 100000 vectors in 128D for training
[2.912 s] Training the index
Training IVF quantizer on 100000 vectors in 128D
Clustering 100000 points in 128D to 1788 clusters, redo 1 times, 10 iterations
  Preprocessing in 0.03 s
Faiss assertion 'err == CUBLAS_STATUS_SUCCESS' failed in void faiss::gpu::runMatrixMult(faiss::gpu::Tensor<T, 2, true>&, bool, faiss::gpu::Tensor<T, 2, true>&, bool, faiss::gpu::Tensor<T, 2, true>&, bool, float, float, bool, cublasHandle_t, cudaStream_t) [with T = float; cublasHandle_t = cublasContext*; cudaStream_t = CUstream_st*] at gpu/utils/MatrixMult.cu:150; details: cublas failed (13): Sgemm (512, 128) x (1788, 128)' = (512, 1788)
Aborted
(faiss-gpu-3.6.3) [hotel-revenue-online@xhy-30-111-42 faiss]$ which gdb
/bin/gdb
(faiss-gpu-3.6.3) [hotel-revenue-online@xhy-30-111-42 faiss]$ gdb
GNU gdb (GDB) Red Hat Enterprise Linux 7.6.1-100.el7
Copyright (C) 2013 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "x86_64-redhat-linux-gnu".
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
(gdb) run ./gpu/test/demo_ivfpq_indexing_gpu
Starting program:  ./gpu/test/demo_ivfpq_indexing_gpu
No executable file specified.
Use the "file" or "exec-file" command.
(gdb) q
(faiss-gpu-3.6.3) [hotel-revenue-online@xhy-30-111-42 faiss]$ gdb ./gpu/test/demo_ivfpq_indexing_gpu
GNU gdb (GDB) Red Hat Enterprise Linux 7.6.1-100.el7
Copyright (C) 2013 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "x86_64-redhat-linux-gnu".
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>...
Reading symbols from /opt/software/faiss/faiss/gpu/test/demo_ivfpq_indexing_gpu...done.
(gdb) run
Starting program: /opt/software/faiss/faiss/./gpu/test/demo_ivfpq_indexing_gpu
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib64/libthread_db.so.1".
[New Thread 0x7fffe451e700 (LWP 3208487)]
[New Thread 0x7fffe3d1d700 (LWP 3208488)]
[New Thread 0x7fffe349b700 (LWP 3208489)]
[2.836 s] Generating 100000 vectors in 128D for training
[2.947 s] Training the index
Training IVF quantizer on 100000 vectors in 128D
Clustering 100000 points in 128D to 1788 clusters, redo 1 times, 10 iterations
  Preprocessing in 0.03 s
Faiss assertion 'err == CUBLAS_STATUS_SUCCESS' failed in void faiss::gpu::runMatrixMult(faiss::gpu::Tensor<T, 2, true>&, bool, faiss::gpu::Tensor<T, 2, true>&, bool, faiss::gpu::Tensor<T, 2, true>&, bool, float, float, bool, cublasHandle_t, cudaStream_t) [with T = float; cublasHandle_t = cublasContext*; cudaStream_t = CUstream_st*] at gpu/utils/MatrixMult.cu:150; details: cublas failed (13): Sgemm (512, 128) x (1788, 128)' = (512, 1788)

Program received signal SIGABRT, Aborted.
0x00007fffebb01207 in raise () from /lib64/libc.so.6
Missing separate debuginfos, use: debuginfo-install glibc-2.17-260.el7_6.3.x86_64 libgcc-4.8.5-36.el7_6.1.x86_64 libgomp-4.8.5-36.el7_6.1.x86_64 libstdc++-4.8.5-36.el7_6.1.x86_64
(gdb) bt
#0  0x00007fffebb01207 in raise () from /lib64/libc.so.6
#1  0x00007fffebb028f8 in abort () from /lib64/libc.so.6
#2  0x0000000000454565 in runMatrixMult<float> (stream=0x2e69050, stream@entry=0x6fc, handle=0x12cc2390,
    useHgemm=<optimized out>, beta=<optimized out>, alpha=<optimized out>, transB=true, b=..., transA=false, a=...,
    transC=<optimized out>, c=...) at gpu/utils/MatrixMult.cu:143
#3  faiss::gpu::runMatrixMult (c=..., transC=transC@entry=false, a=..., transA=transA@entry=false, b=...,
    transB=transB@entry=true, alpha=alpha@entry=-2, beta=beta@entry=0, useHgemm=useHgemm@entry=false, handle=0x12cc2390,
    stream=stream@entry=0x2e69050) at gpu/utils/MatrixMult.cu:162
#4  0x000000000051cf36 in faiss::gpu::runDistance<float> (resources=0x7fffffffdbc0, centroids=..., centroidsRowMajor=true,
    centroidNorms=centroidNorms@entry=0x12d322e8, queries=..., queriesRowMajor=queriesRowMajor@entry=true, k=1,
    outDistances=..., outIndices=..., ignoreOutDistances=false, useHgemm=false, computeL2=true) at gpu/impl/Distance.cu:285
#5  0x000000000051d7a5 in runL2Distance<float> (ignoreOutDistances=<optimized out>, ignoreOutDistances@entry=false,
    useHgemm=false, outIndices=..., outDistances=..., k=k@entry=1, queriesRowMajor=queriesRowMajor@entry=true, queries=...,
    centroidNorms=centroidNorms@entry=0x12d322e8, centroidsRowMajor=<optimized out>, centroids=..., resources=<optimized out>)
    at gpu/impl/Distance.cu:492
#6  faiss::gpu::runL2Distance (resources=<optimized out>, vectors=..., vectorsRowMajor=<optimized out>,
    vectorNorms=vectorNorms@entry=0x12d322e8, queries=..., queriesRowMajor=queriesRowMajor@entry=true, k=k@entry=1,
    outDistances=..., outIndices=..., ignoreOutDistances=<optimized out>, ignoreOutDistances@entry=false)
    at gpu/impl/Distance.cu:493
#7  0x000000000044a500 in faiss::gpu::FlatIndex::query (this=0x12d32190, input=..., k=k@entry=1, outDistances=...,
    outIndices=..., exactDistance=exactDistance@entry=true) at gpu/impl/FlatIndex.cu:132
#8  0x000000000042fb7c in faiss::gpu::GpuIndexFlat::searchImpl_ (this=0x12d32130, n=100000, x=<optimized out>, k=1,
    distances=<optimized out>, labels=0x7fff40061a80) at gpu/GpuIndexFlat.cu:212
#9  0x000000000042a89d in faiss::gpu::GpuIndex::searchNonPaged_ (this=0x12d32130, n=100000, x=0x7fff3cf2b010, k=1,
    outDistancesData=0x7fff40000000, outIndicesData=0x7fff40061a80) at gpu/GpuIndex.cu:269
#10 0x000000000042be9a in faiss::gpu::GpuIndex::search (this=0x12d32130, n=100000, x=0x7fff3cf2b010, k=1, distances=0x12df5880,
    labels=0x12d32370) at gpu/GpuIndex.cu:243
#11 0x00000000004aca87 in faiss::Clustering::train (this=this@entry=0x7fffffffd930, nx=nx@entry=100000,
    x_in=x_in@entry=0x7fff3cf2b010, index=...) at Clustering.cpp:194
---Type <return> to continue, or q <return> to quit---
#12 0x0000000000435acf in faiss::gpu::GpuIndexIVF::trainQuantizer_ (this=this@entry=0x7fffffffdb00, n=n@entry=100000,
    x=0x7fff3cf2b010) at gpu/GpuIndexIVF.cu:237
#13 0x0000000000438268 in faiss::gpu::GpuIndexIVFPQ::train (this=this@entry=0x7fffffffdb00, n=n@entry=100000, x=0x7fff3cf2b010)
    at gpu/GpuIndexIVFPQ.cu:317
#14 0x0000000000408efe in main () at demo_ivfpq_indexing_gpu.cpp:81


[hotel-revenue-online@xhy-30-111-42 faiss]$ ldd gpu/test/demo_ivfpq_indexing_gpu
	linux-vdso.so.1 =>  (0x00007ffdeffc1000)
	/opt/share/lib64/mkl_linux/lib/libmkl_core.so (0x00007f9a3d977000)
	/opt/share/lib64/mkl_linux/lib/libmkl_sequential.so (0x00007f9a3c3de000)
	libmkl_intel_lp64.so => /opt/share/lib64/mkl_linux/lib/libmkl_intel_lp64.so (0x00007f9a3b8ad000)
	libmkl_gnu_thread.so => /opt/share/lib64/mkl_linux/lib/libmkl_gnu_thread.so (0x00007f9a3a074000)
	libgomp.so.1 => /lib64/libgomp.so.1 (0x00007f9a39e40000)
	libpthread.so.0 => /lib64/libpthread.so.0 (0x00007f9a39c24000)
	libdl.so.2 => /lib64/libdl.so.2 (0x00007f9a39a20000)
	libcudart.so.9.0 => /usr/local/cuda-9.0/lib64/libcudart.so.9.0 (0x00007f9a397b2000)
	libcublas.so.9.0 => /usr/local/cuda-9.0/lib64/libcublas.so.9.0 (0x00007f9a3637c000)
	libstdc++.so.6 => /lib64/libstdc++.so.6 (0x00007f9a36075000)
	libm.so.6 => /lib64/libm.so.6 (0x00007f9a35d72000)
	libgcc_s.so.1 => /lib64/libgcc_s.so.1 (0x00007f9a35b5c000)
	libc.so.6 => /lib64/libc.so.6 (0x00007f9a3578f000)
	/lib64/ld-linux-x86-64.so.2 (0x000056096363d000)
	librt.so.1 => /lib64/librt.so.1 (0x00007f9a35586000)

```

# rerenece
[Different CUDA versions shown by nvcc and NVIDIA-smi](https://stackoverflow.com/questions/53422407/different-cuda-versions-shown-by-nvcc-and-nvidia-smi)

[faiss::gpu::runMatrixMult failure #34](https://github.com/facebookresearch/faiss/issues/34)

[CUDA Toolkit Archive](https://developer.nvidia.com/cuda-toolkit-archive)
