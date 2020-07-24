# package

因为网络特殊原因，所以树莓派上运行的opencv-python的arm版本的whl文件进行保存。
如果需要pip下载这个包，则需要添加pip源：**/etc/pip.conf**

```shell script
[global]
timeout =6000
index-url =http://pypi.douban.com/simple/
# 声明树莓派arm源，否则安装opencv-python失败
extra-index-url=https://www.piwheels.org/simple
[install]
use-mirrors =true
mirrors =http://pypi.douban.com/simple/
trusted-host =pypi.douban.com
```
## 安装opencv-python

### pip

通过pip安装，网络情况较好可以选择

```shell script
pip install opencv-python
```
### 手动安装

目录下提供了三个版本的opencv_python-4.1.1.26，分别对应python34，python35，python37，根据自己需求选择，如果没有合适的，可以去[网站](https://www.piwheels.org/project/opencv-python/)选择。

opencv_python-4.1.1.26-cp37-cp37m-linux_armv7l.whl，这个是python37的opencv_python-4.1.1.26版本的arm7架构的包，官方已经编译完成的，最新版本则需要自己编译。

```shell script
# 我的树莓派版本是python37，arm7架构，因此选择安装这个whl包
pip install opencv_python-4.1.1.26-cp37-cp37m-linux_armv7l.whl
```

如果不出意外的话，会出现如下错误：（当然没有错误就更好了，可以看运行章节）

```shell
(venv) root@raspberrypi:/home/respberry-flask/venv/lib/python3.7/site-packages/cv2# ldd cv2.cpython-37m-arm-linux-gnueabihf.so  | grep "not found"
./cv2.cpython-37m-arm-linux-gnueabihf.so: /lib/arm-linux-gnueabihf/libm.so.6: version `GLIBC_2.27' not found (required by ./cv2.cpython-37m-arm-linux-gnueabihf.so)
./cv2.cpython-37m-arm-linux-gnueabihf.so: /lib/arm-linux-gnueabihf/libc.so.6: version `GLIBC_2.28' not found (required by ./cv2.cpython-37m-arm-linux-gnueabihf.so)
        libIlmImf-2_2.so.23 => not found
        libIex-2_2.so.23 => not found
        libHalf.so.23 => not found
        libIlmThread-2_2.so.23 => not found
        libavcodec.so.58 => not found
        libavformat.so.58 => not found
        libavutil.so.56 => not found
        libswscale.so.5 => not found
```

出现动态链接库无法找到，如果出现这个问题，那么就请继续往下看，开始编译安装opencv库来解决这个问题。

## 编译安装opencv

### 下载opencv

```shell
mkdir ~/opencv_build && cd ~/opencv_build
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git
```

克隆存储库后，创建一个临时构建目录，然后切换到该目录：

```shell
mkdir -p ~/opencv_build/opencv/build
cd ~/opencv_build/opencv/build
```

### 编译参数

```shell
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_build/opencv_contrib/modules/ \
    -D PYTHON3_EXECUTABLE=/usr/local/python3.7/bin/python3.7 \
    -D PYTHON3_INCLUDE_DIR=/usr/local/python3.7/include/python3.7m \
    -D PYTHON3_LIBRARY=/usr/lib/arm-linux-gnueabihf/libpython3.7m.a \
    -D PYTHON3_NUMPY_INCLUDE_DIRS=/usr/local/python3.7/lib/python3.7/site-packages/numpy/core/include \
    -D PYTHON_DEFAULT_AVAILABLE=/usr/local/python3.7 \
    -D BUILD_EXAMPLES=OFF ..

CMAKE_BUILD_TYPE=RELEASE \ 代表编译类型为发行版本
CMAKE_INSTALL_PREFIX=/usr/local \ 安装路径
INSTALL_C_EXAMPLES=ON \ C demo
INSTALL_PYTHON_EXAMPLES=ON \ Python demo
OPENCV_EXTRA_MODULES_PATH=/home/pi/.../opencv/opencv_contrib/modules \ OpenCV Contrib路径
BUILD_EXAMPLES=ON \ 编译demo
WITH_LIBV4L=ON \ 开启Video for Linux
PYTHON3_EXECUTABLE=/usr/bin/python3.7 \ Python3.7路径
PYTHON_INCLUDE_DIR=/usr/local/python3.7/include \ Python3.7 include文件夹
PYTHON_LIBRARY=/usr/lib/arm-linux-gnueabihf/libpython3.7m.so \ Python3.7库
PYTHON3_NUMPY_INCLUDE_DIRS=/usr/lib/python3/dist-packages/numpy/core/include \ Python3 Numpy安装路径
```

### 编译

```shell
make -j4
```

### 安装

```shell
make install
```

### 检查opencv

```shell
pkg-config --modversion opencv4
4.1.1
```

### 检查Python import

```shell
python3.7 -c "import cv2; print(cv2.__version__)"
```

