# package

​		因为网络特殊原因，所以树莓派上运行的opencv-python的arm版本的whl文件进行保存。
​		如果需要pip下载这个包，则需要添加pip源：/etc/pip.conf

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
## 安装

​		通过pip安装，网络情况较好可以选择

```shell script
pip install opencv-python
```
​		手动安装

​		目录下提供了三个版本的opencv_python-4.1.1.26，分别对应python34，python35，python37，根据自己需求选择，如果没有合适的，可以去[网站](https://www.piwheels.org/project/opencv-python/)选择。

​		opencv_python-4.1.1.26-cp37-cp37m-linux_armv7l.whl，这个是python37的opencv_python-4.1.1.26版本的arm7架构的包，官方已经编译完成的，最新版本则需要自己编译。

```shell script
# 我的树莓派版本是python37，arm7架构，因此选择安装这个whl包
pip install opencv_python-4.1.1.26-cp37-cp37m-linux_armv7l.whl
```

