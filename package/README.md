# package

因为网络特殊原因，所以树莓派上运行的opencv-python的arm版本的whl文件进行保存。
如果需要pip下载这个包，则需要添加pip源：/etc/pip.conf
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
安装
```shell script
pip install opencv-python
```
或者手动安装opencv_python-4.1.1.26-cp37-cp37m-linux_armv7l.whl，这个是python37的opencv_python-4.1.1.26版本包，官方已经编译完成的，最新版本则需要自己编译。