# respberry-flask

不要被这个名称吓坏了，在后面的更新当中，把flask框架去掉了，里面目前只是包含了mqtt库以及apschedule库。

这个项目包含远程GPIO控制+运动物体检测。

- 在树莓派端启动。
- 树莓派摄像头。
- python3.7。
- opencv。

## 环境

- emqx服务器。
- opencv最新版本源码编译。

## 下载源码

```shell
git clone https://github.com/ranzhendong/respberry-flask.git
```

## 创建虚拟环境

```shell
cd respberry-flask
python -m venv venv
```

## 安装依赖

​		需要注意的是：部分依赖在pycharm开发，也就是macos上是不支持的，因为x86可能没有这样的包，但是在代码运行过程当中，还是需要这些包的，因此将它手动添加到requirements.txt当中。

```shell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 启动

需要在flaskr文件夹下面启动。

```shell script
python respberry.py
```

