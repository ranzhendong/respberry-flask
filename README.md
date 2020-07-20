# respberry-flask

这个项目是需要在树莓派端启动的，用于订阅emqx消息，根据消息的不同，作出不同的动作。

## 环境

- python3.7
- emqx部署

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

## 启动flask

需要在flaskr文件夹下面启动，默认读取config.py配置文件

```shell script
gunicorn -c config.py respberry:app
```

