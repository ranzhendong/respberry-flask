# respberry-flask
 
启动flask项目
需要在flaskr文件夹下面启动，默认读取config.py配置文件
```shell script
gunicorn -c config.py respberry:app
```