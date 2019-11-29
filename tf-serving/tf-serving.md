
[TOC]

# TF-Serving

## docker compile
### 1.14 compile

```bash
# docker comile Dockerfile
# compile devel env
nohup docker build --no-cache -t centos-base-env:v0 -f Dockerfile.devel-mkl-centos . > ./build.log 2>&1 &
# compile deploy env
docker build -t tf-serving:v1.14 -f Dockerfile.mkl-centos .


# docker 环境中验证
tensorflow_model_server --port=8500 --rest_api_port=8501 --model_name=half_plus_two --model_base_path=/opt/serving/serving/tensorflow_serving/servables/tensorflow/testdata/half_plus_two

tensorflow_model_server --port=8500 --rest_api_port=8501 --model_name=half_plus_two --model_base_path=/serving/tensorflow_serving/servables/tensorflow/testdata/half_plus_two

# RESTfull API validate
curl -i -H "Content-Type:application/json" -d '{"instances": [1.0, 2.0, 5.0]}' -X POST 'http://127.0.0.1:8501/v1/models/half_plus_two:predict'

# test example
# start service
cd $HOME/app/serving
docker run -p 8501:8501 -p 8500:8500 --mount type=bind,source=/opt/serving/serving/tensorflow_serving/servables/tensorflow/testdata/half_plus_two,target=/models/half_plus_two -e MODEL_NAME=half_plus_two -t tf-serving:v1.14

# RESTfull API validate
curl -i -H "Content-Type:application/json" -d '{"instances": [1.0, 2.0, 5.0]}' -X POST 'http://127.0.0.1:8501/v1/models/half_plus_two:predict'

# 查看模型结构
curl http://localhost:8501/v1/models/tf_model_test/metadata

```


## source compile

[TensorFlow Serving 安装总结](https://zhuanlan.zhihu.com/p/55108743)

[tensorflow serving目录解读](http://www.mamicode.com/info-detail-2106743.html)

[TensorFlow Serving入门](https://www.jianshu.com/p/afe80b2ed7f0)

[美团基于TensorFlow Serving的深度学习在线预估](https://tech.meituan.com/2018/10/11/tfserving-improve.html)

[TensorFlow* Optimizations on Modern Intel® Architecture](https://software.intel.com/en-us/articles/tensorflow-optimizations-on-modern-intel-architecture)

[TensorFlow学习笔记](https://bookdown.org/leovan/TensorFlow-Learning-Notes/4-5-deploy-tensorflow-serving.html)

[TF-Serving使用Batch提升性能](https://www.dearcodes.com/index.php/archives/36/)

[[译]TensorFlow Serving RESTful API](https://www.jianshu.com/p/a9dbf1e63c88?utm_source=oschina-app)

[使用 TensorFlow Serving 和 Docker 快速部署机器学习服务(Keras)](https://segmentfault.com/a/1190000018378850)

[keras、tensorflow serving踩坑](https://blog.csdn.net/qq_34106574/article/details/82870416)

[keras模型转 tensorflow模型](http://xcx1024.com/ArtInfo/83289.html)

[在Docker中使用Tensorflow Serving(nvidia docker)](http://fancyerii.github.io/books/tfserving-docker/)

[TensorFlow 模型如何对外提供服务](http://shzhangji.com/cnblogs/2018/05/14/serve-tensorflow-estimator-with-savedmodel/)

[How to publish custom (non-tensorflow) models using tensorflow-serving](https://stackoverflow.com/questions/49571655/how-to-publish-custom-non-tensorflow-models-using-tensorflow-serving)

[Tensorflow Serving 介绍](https://blog.csdn.net/zwqjoy/article/details/82762207)

[Deploying Machine Learning Models in Practice](https://qconsp.com/sp2018/system/files/presentation-slides/qconsp18-deployingml-may18-npentreath.pdf)

[Saving custom estimators in TensorFlow](https://stackoverflow.com/questions/47856879/saving-custom-estimators-in-tensorflow)

[TensorFlow v1.10+ Serving Custom Estimator](https://stackoverflow.com/questions/53356029/tensorflow-v1-10-serving-custom-estimator)

[45532epigramai/tfserving-python-predict-client](https://github.com/epigramai/tfserving-python-predict-client)

[tensorflow serving 动态加载更新模型](https://blog.csdn.net/hahajinbu/article/details/81945149)

[Best practice: loading new models during runtime (not versions) #422](https://github.com/tensorflow/serving/issues/422)

[Make ModelServer poll for model_config changes from remote (e.g. S3) location #1301](https://github.com/tensorflow/serving/issues/1301)

### 1.12 compile
```bash
# basic dependence

# Build Esentials (minimal)
sudo yum -y install gcc gcc-c++ kernel-devel make automake autoconf swig git unzip libtool binutils patch wget bzip2

# Extra Packages for Enterprise Linux (EPEL) (for pip, zeromq3)
sudo yum -y install epel-release centos-release-scl

# HTTP2 Curl
sudo yum -y install libev libev-devel zlib zlib-devel openssl openssl-devel

# conda install
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-5.3.1-Linux-x86_64.sh
sh Anaconda3-5.3.1-Linux-x86_64.sh

# Other TF deps
sudo yum -y install freetype-devel libpng12-devel zip zlib-devel giflib-devel zeromq3-devel
pip install grpcio_tools
pip install mock
pip install grpcio
pip install h5py
pip install keras_applications
pip install keras_preprocessing
pip install opencv-python
pip install tensorflow==1.14.0
pip install tensorflow-serving-api==1.14.0

# install bazel
sh ./bazel-0.19.2-installer-linux-x86_64.sh --prefix=/opt/app/bazel19
export PATH=$PATH:/opt/app/bazel19/bin
bazel version

# tf serving download
git clone -b r1.12 --recurse-submodules https://github.com/tensorflow/serving

# serving/tools下面bazel.rc移动到serving/下面
mv tools/bazel.rc ../.bazelrc

# compile tf-serving
bazel build -c opt --copt=-mavx --copt=-mavx2 --copt=-msse4.1 --copt=-msse4.2 --copt=-mfma --copt=-mfpmath=both --local_resources 8192,.5,1.0 --verbose_failures --action_env PYTHON_BIN_PATH=/opt/app/anaconda3/bin/python --action_env PYTHON_LIB_PATH=/opt/app/anaconda3/lib/python3.7/site-packages --define PYTHON_BIN_PATH=/opt/app/anaconda3/bin/python --define PYTHON_LIB_PATH=/opt/app/anaconda3/lib/python3.7/site-packages  --python_path=/opt/app/anaconda3/bin/python --force_python=py3 --host_force_python=py3 --define with_jemalloc=true --define with_gcp_support=true tensorflow_serving/...

bazel build -c opt --copt=-mavx --copt=-mavx2 --copt=-msse4.1 --copt=-msse4.2 --copt=-mfma --copt=-mfpmath=both --config=nativeopt --local_resources 8192,.5,1.0 --verbose_failures --action_env PYTHON_BIN_PATH=/opt/app/anaconda3/bin/python --action_env PYTHON_LIB_PATH=/opt/app/anaconda3/lib/python3.7/site-packages --define PYTHON_BIN_PATH=/opt/app/anaconda3/bin/python --define PYTHON_LIB_PATH=/opt/app/anaconda3/lib/python3.7/site-packages  --python_path=/opt/app/anaconda3/bin/python --force_python=py3 --host_force_python=py3 --define with_jemalloc=true --define with_gcp_support=true tensorflow_serving/...


# tensorflow_serving/model_servers:tensorflow_model_server
bazel build -c opt --copt=-mavx --copt=-mavx2 --copt=-msse4.1 --copt=-msse4.2 --copt=-mfma --copt=-mfpmath=both --local_resources 8192,.5,1.0 --verbose_failures --action_env PYTHON_BIN_PATH=/opt/app/anaconda3/bin/python --action_env PYTHON_LIB_PATH=/opt/app/anaconda3/lib/python3.7/site-packages --define PYTHON_BIN_PATH=/opt/app/anaconda3/bin/python --define PYTHON_LIB_PATH=/opt/app/anaconda3/lib/python3.7/site-packages  --python_path=/opt/app/anaconda3/bin/python --force_python=py3 --host_force_python=py3 --define with_jemalloc=true --define with_gcp_support=true tensorflow_serving/model_servers:tensorflow_model_server | tee -a build.log

################################################################################################
# test example
# start service
bazel-bin/tensorflow_serving/model_servers/tensorflow_model_server --port=8500 --rest_api_port=8501 --model_name=half_plus_two --model_base_path=/opt/app/serving/tensorflow_serving/servables/tensorflow/testdata/half_plus_two

# RESTfull API validate
curl -i -H "Content-Type:application/json" -d '{"instances": [1.0, 2.0, 5.0]}' -X POST 'http://127.0.0.1:8501/v1/models/half_plus_two:predict'

# gRPR API validate
cd serving
python tensorflow_serving/example/mnist_client.py --num_tests=1000 --server=127.0.0.1:8500


# docker run -p 8501:8501 \
  --mount type=bind,\
   source=/tmp/tfserving/serving/tensorflow_serving/servables/tensorflow/testdata/saved_model_half_plus_two_cpu,\
target=/models/half_plus_two \
-e MODEL_NAME=half_plus_two -t tensorflow/serving &

# python tensorflow_serving/example/mnist_saved_model.py /tmp/models/mnist


```

#### problem

##### instructions

```bash
Your CPU supports instructions that this TensorFlow binary was not compiled to use: SSE4.1 SSE4.2 AVX

Solution：--copt=-mavx --copt=-mavx2 --copt=-msse4.1 --copt=-msse4.2 --copt=-mfma --copt=-mfpmath=both
https://stackoverflow.com/questions/41293077/how-to-compile-tensorflow-with-sse4-2-and-avx-instructions

https://blog.csdn.net/dQCFKyQDXYm3F8rB0/article/details/88967608
```

##### 在WORKSPACE中增加 "http_archive" 配置
```bash
ERROR: /opt/app/serving/WORKSPACE:20:1: name 'http_archive' is not defined
ERROR: Error evaluating WORKSPACE file
ERROR: error loading package '': in /opt/app/serving/tensorflow_serving/workspace.bzl: Encountered error while reading extension file 'tensorflow/workspace.bzl': no such package '@org_tensorflow//tensorflow': error loading package 'external': Could not load //external package
ERROR: error loading package '': in /opt/app/serving/tensorflow_serving/workspace.bzl: Encountered error while reading extension file 'tensorflow/workspace.bzl': no such package '@org_tensorflow//tensorflow': error loading package 'external': Could not load //external package
INFO: Elapsed time: 0.165s
INFO: 0 processes.
FAILED: Build did NOT complete successfully (0 packages loaded)

Solution：
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
```

##### bazel版本导致问题
```bash
ERROR: error loading package '': in /opt/app/serving/tensorflow_serving/workspace.bzl: in /opt/.cache/bazel/_bazel_yunwei/b97158e17fffa263a058f3a45ad6ebae/external/org_tensorflow/tensorflow/workspace.bzl: Label '@org_tensorflow//third_party:nccl/nccl_configure.bzl' crosses boundary of subpackage '@org_tensorflow//third_party/nccl' (perhaps you meant to put the colon here: '@org_tensorflow//third_party/nccl:nccl_configure.bzl'?)
ERROR: error loading package '': in /opt/app/serving/tensorflow_serving/workspace.bzl: in /opt/.cache/bazel/_bazel_yunwei/b97158e17fffa263a058f3a45ad6ebae/external/org_tensorflow/tensorflow/workspace.bzl: Label '@org_tensorflow//third_party:nccl/nccl_configure.bzl' crosses boundary of subpackage '@org_tensorflow//third_party/nccl' (perhaps you meant to put the colon here: '@org_tensorflow//third_party/nccl:nccl_configure.bzl'?)

Solution：将bazel 0.28.1版本降低至0.19.2版本
```

##### Wno-shift-negative-value err
```bash
cc1plus: warning: unrecognized command line option "-Wno-shift-negative-value" [enabled by default]

```

##### bazel 版本导致的问题

```bash
ERROR: /opt/.cache/bazel/_bazel_yunwei/b97158e17fffa263a058f3a45ad6ebae/external/com_github_libevent_libevent/BUILD.bazel:52:1: Executing genrule @com_github_libevent_libevent//:libevent-srcs failed (Exit 1) bash failed: error executing command
  (cd /opt/.cache/bazel/_bazel_yunwei/b97158e17fffa263a058f3a45ad6ebae/execroot/tf_serving & \
  exec env - \
    PATH=/opt/app/anaconda3/bin:/opt/app/bazel19/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/.local/bin:/opt/bin \
    PYTHON_BIN_PATH=/opt/app/anaconda3/bin/python \
    PYTHON_LIB_PATH=/opt/app/anaconda3/lib/python3.7/site-packages)

Solution: https://github.com/tensorflow/serving/pull/1066
mv tools/bazel.rc ../.bazelrc

Old bazel used to read %workspace%/tools/bazel.rc. New bazel will not
read that and instead will only read %workspace%/.bazelrc.
```


### 1.13 compile
```bash
export TEST_TMPDIR=/opt/.cache0.20.0
export PATH=/opt/app/bazel-0.20.0/bin:$PATH

```

#### problem

##### nccl 

```bash
ERROR: error loading package '': in /opt/app/serving1.13/serving/tensorflow_serving/workspace.bzl: in /opt/.cache0.28.1/_bazel_yunwei/b2720352514e02df0d92719be97c37f6/external/org_tensorflow/tensorflow/workspace.bzl: Label '@org_tensorflow//third_party:nccl/nccl_configure.bzl' crosses boundary of subpackage '@org_tensorflow//third_party/nccl' (perhaps you meant to put the colon here: '@org_tensorflow//third_party/nccl:nccl_configure.bzl'?)
ERROR: error loading package '': in /opt/app/serving1.13/serving/tensorflow_serving/workspace.bzl: in /opt/.cache0.28.1/_bazel_yunwei/b2720352514e02df0d92719be97c37f6/external/org_tensorflow/tensorflow/workspace.bzl: Label '@org_tensorflow//third_party:nccl/nccl_configure.bzl' crosses boundary of subpackage '@org_tensorflow//third_party/nccl' (perhaps you meant to put the colon here: '@org_tensorflow//third_party/nccl:nccl_configure.bzl'?)
INFO: Elapsed time: 2.546s
INFO: 0 processes.
FAILED: Build did NOT complete successfully (0 packages loaded)


Solution: https://stackoverflow.com/questions/56476405/issue-in-building-tensorboard-1-13-1-from-source-cfg-must-be-either-host-or
https://github.com/tensorflow/tensorflow/commit/2243bd6ba9b36d43dbd5c0ede313853f187f5dce

modify /opt/.cache0.28.1/_bazel_yunwei/b2720352514e02df0d92719be97c37f6/external/org_tensorflow/tensorflow/workspace.bzl
# load("//third_party:nccl/nccl_configure.bzl", "nccl_configure")
load("//third_party/nccl:nccl_configure.bzl", "nccl_configure")

```

##### gpus
```bash
ERROR: /opt/.cache0.25.3/_bazel_yunwei/b2720352514e02df0d92719be97c37f6/external/org_tensorflow/third_party/gpus/cuda_configure.bzl:115:1: load() statements must be called before any other statement. First non-load() statement appears at /opt/.cache0.25.3/_bazel_yunwei/b2720352514e02df0d92719be97c37f6/external/org_tensorflow/third_party/gpus/cuda_configure.bzl:26:1. Use --incompatible_bzl_disallow_load_after_statement=false to temporarily disable this check.
INFO: An error occurred during the fetch of repository 'io_bazel_rules_closure'
INFO: Call stack for the definition of repository 'io_bazel_rules_closure':
 - /opt/app/serving1.13/serving/WORKSPACE:22:1
ERROR: error loading package '': in /opt/app/serving1.13/serving/tensorflow_serving/workspace.bzl: in /opt/.cache0.25.3/_bazel_yunwei/b2720352514e02df0d92719be97c37f6/external/org_tensorflow/tensorflow/workspace.bzl: Extension 'third_party/gpus/cuda_configure.bzl' has errors
ERROR: error loading package '': in /opt/app/serving1.13/serving/tensorflow_serving/workspace.bzl: in /opt/.cache0.25.3/_bazel_yunwei/b2720352514e02df0d92719be97c37f6/external/org_tensorflow/tensorflow/workspace.bzl: Extension 'third_party/gpus/cuda_configure.bzl' has errors
INFO: Elapsed time: 3.293s

Solution: https://github.com/tensorflow/tensorflow/commit/494d2cc5cfd04c3c376f10b7d7c417e388b08282

vim /opt/.cache0.25.3/_bazel_yunwei/b2720352514e02df0d92719be97c37f6/external/org_tensorflow/third_party/gpus/cuda_configure.bzl

将这段代码移动配置文件最开始
load("//third_party/clang_toolchain:download_clang.bzl", "download_clang")
load(
    "@bazel_tools//tools/cpp:lib_cc_configure.bzl",
    "escape_string",
    "get_env_var",
)
load(
    "@bazel_tools//tools/cpp:windows_cc_configure.bzl",
    "find_msvc_tool",
    "find_vc_path",
    "setup_vc_env_vars",
)


修改：
将 if inc not in includes_cpp_set 修改为 if inc not in includes_cpp_set.to_list()

```

### 1.14 compile
```bash
# install bazel
sh ./bazel-0.24.1-installer-linux-x86_64.sh --prefix=/opt/app/bazel
export PATH=/opt/app/bazel-0.24.1/bin:$PATH
export TEST_TMPDIR=/opt/.cache0.24.1
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/app/anaconda3/pkgs/openssl-1.0.2l-0/lib
bazel version

# tf serving download
git clone -b r1.14 --recurse-submodules https://github.com/tensorflow/serving.git

# compile tf-serving
bazel build -c opt --config=nativeopt --local_resources 8192,.5,1.0 --verbose_failures --action_env PYTHON_BIN_PATH=/opt/app/anaconda3/bin/python --action_env PYTHON_LIB_PATH=/opt/app/anaconda3/lib/python3.7/site-packages --define PYTHON_BIN_PATH=/opt/app/anaconda3/bin/python --define PYTHON_LIB_PATH=/opt/app/anaconda3/lib/python3.7/site-packages  --python_path=/opt/app/anaconda3/bin/python --force_python=py3 --host_force_python=py3 --define with_jemalloc=true --define with_gcp_support=true tensorflow_serving/...


# tensorflow_serving/model_servers:tensorflow_model_server
bazel build -c opt --copt=-mavx --copt=-mavx2 --copt=-msse4.1 --copt=-msse4.2 --copt=-mfma --copt=-mfpmath=both --local_resources 8192,.5,1.0 --verbose_failures --action_env PYTHON_BIN_PATH=/opt/app/anaconda3/bin/python --action_env PYTHON_LIB_PATH=/opt/app/anaconda3/lib/python3.7/site-packages --define PYTHON_BIN_PATH=/opt/app/anaconda3/bin/python --define PYTHON_LIB_PATH=/opt/app/anaconda3/lib/python3.7/site-packages  --python_path=/opt/app/anaconda3/bin/python --force_python=py3 --host_force_python=py3 --define with_jemalloc=true --define with_gcp_support=true tensorflow_serving/model_servers:tensorflow_model_server | tee -a build.log

bazel build -c opt --copt=-mavx --copt=-msse4.1 --copt=-msse4.2 --local_resources 8192,.5,1.0 --verbose_failures --action_env PYTHON_BIN_PATH=/opt/app/anaconda3/bin/python --action_env PYTHON_LIB_PATH=/opt/app/anaconda3/lib/python3.7/site-packages --define PYTHON_BIN_PATH=/opt/app/anaconda3/bin/python --define PYTHON_LIB_PATH=/opt/app/anaconda3/lib/python3.7/site-packages  --python_path=/opt/app/anaconda3/bin/python --force_python=py3 --host_force_python=py3 --define with_jemalloc=true --define with_gcp_support=true tensorflow_serving/model_servers:tensorflow_model_server | tee -a build.log

#  --config=mkl --copt="-DEIGEN_USE_VML"
export PATH=/opt/app/bazel-0.24.1/bin:$PATH
export TEST_TMPDIR=/opt/.cache0.24.1.mkl
nohup bazel build -c opt --config=mkl --config=nativeopt --copt="-DEIGEN_USE_VML" --copt=-mavx --copt=-msse4.1 --copt=-msse4.2 --local_resources 8192,.5,1.0 --verbose_failures --action_env PYTHON_BIN_PATH=/opt/app/anaconda3/bin/python --action_env PYTHON_LIB_PATH=/opt/app/anaconda3/lib/python3.7/site-packages --define PYTHON_BIN_PATH=/opt/app/anaconda3/bin/python --define PYTHON_LIB_PATH=/opt/app/anaconda3/lib/python3.7/site-packages  --python_path=/opt/app/anaconda3/bin/python --force_python=py3 --host_force_python=py3 --define with_jemalloc=true --define with_gcp_support=true tensorflow_serving/model_servers:tensorflow_model_server > build.log 2>&1 &

################################################################################################
# test example
# start service
bazel-bin/tensorflow_serving/model_servers/tensorflow_model_server --port=8500 --rest_api_port=8501 --model_name=half_plus_two --model_base_path=/opt/app/serving1.14/serving/tensorflow_serving/servables/tensorflow/testdata/half_plus_two

# RESTfull API validate
curl -i -H "Content-Type:application/json" -d '{"instances": [1.0, 2.0, 5.0]}' -X POST 'http://127.0.0.1:8501/v1/models/half_plus_two:predict'

# gRPR API validate
# https://www.tensorflow.org/tfx/serving/serving_basic
cd serving
python tensorflow_serving/example/mnist_saved_model.py /tmp/models/mnist

bazel-bin/tensorflow_serving/model_servers/tensorflow_model_server --port=8500 --rest_api_port=8501 --model_name=mnist --model_base_path=/tmp/models/mnist
python tensorflow_serving/example/mnist_client.py --num_tests=1000 --server=127.0.0.1:8500
```



# grpc

http://www.grpc.io/
https://github.com/grpc/grpc-java
https://www.grpc.io/docs/tutorials/basic/java/
http://www.grpc.io/docs/tutorials/basic/java.html
https://github.com/kaiwaehner/tensorflow-serving-java-grpc-kafka-streams
https://github.com/junwan01/tensorflow-serve-client

[tensorflow serving 服务部署与访问（Python + Java）](https://blog.csdn.net/shin627077/article/details/78592729)

[Java和Python使用Grpc访问Tensorflow的Serving代码](http://www.manongjc.com/article/110876.html)

[GRPC原理解析](https://www.iteye.com/blog/shift-alt-ctrl-2292862)

https://tbr8.org/java-invoke-tfserving-model/

# other technology

## SSE VS AVX

SSE(Streaming SIMD Extensions)是英特尔在AMD的3DNow!发布一年之后，在其计算机芯片Pentium III中引入的指令集，是继MMX的扩充指令集

AVX(Advanced Vector Extensions) 是Intel的SSE延伸架构

FMA是Intel的AVX扩充指令集，如名称上熔合乘法累积（Fused Multiply Accumulate）的意思一样

3DNow!（据称是“3D No Waiting!”的缩写）是由AMD开发的一套SIMD多媒体指令集，支持单精度浮点数的矢量运算，用于增强x86架构的计算机在三维图像处理上的性能

[SIMD、MMX、SSE、AVX、3D Now！、neon](https://blog.csdn.net/conowen/article/details/7255920)

[SIMD 指令集介绍](https://blog.csdn.net/woxiaohahaa/article/details/51014425)

[单线程、SSE、AVX运行效率对比——加法运算](https://blog.csdn.net/samylee/article/details/88874899)

[使用Intel SSE/AVX指令集（SIMD）加速向量内积计算](https://zhoujianshi.github.io/articles/2017/%E4%BD%BF%E7%94%A8Intel%20SSE-AVX%E6%8C%87%E4%BB%A4%E9%9B%86%EF%BC%88SIMD%EF%BC%89%E5%8A%A0%E9%80%9F%E5%90%91%E9%87%8F%E5%86%85%E7%A7%AF%E8%AE%A1%E7%AE%97/index.html)

[SIMD简介](https://zhuanlan.zhihu.com/p/55327037)

[Model Serving: Stream Processing vs. RPC/REST With Java, gRPC, Apache Kafka, TensorFlow](https://dzone.com/articles/model-serving-stream-processing-vs-rpc-rest-with-j)

[Tensorflow serving: REST vs gRPC](https://medium.com/@avidaneran/tensorflow-serving-rest-vs-grpc-e8cef9d4ff62)

[TensorFlow Serving 101 pt. 2](https://medium.com/epigramai/tensorflow-serving-101-pt-2-682eaf7469e7)
