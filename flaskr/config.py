import multiprocessing

bind = "127.0.0.1:8001"
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 1
backlog = 2048
worker_class = "gevent"
worker_connections = 1000
daemon = False
debug = True
proc_name = "respberry"
# pidfile = './log/gunicorn.pid'
# errorlog = './log/gunicorn.log'
