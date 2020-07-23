#!/usr/bin/env python3
import datetime
import json
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from flaskr.motion.motion_detection import Motion
from picamera.array import PiRGBArray
from picamera import PiCamera
from flask import Flask
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# emqx host

Host = "emqx.ranzhendong.com.cn"
# emqx port
Port = 1883
# Relay physical pin
Light = 35
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
# Pin status is set to output
GPIO.setup(Light, GPIO.OUT)

# # flask
# app = Flask(__name__)
# app.config.from_object("config")
#
#
# @app.route("/")
# def hello_world():
#     return "Hello, World!"


# Set the pin to low level
def openLight():
    GPIO.output(Light, GPIO.LOW)


# Set the pin to high level
def closeLight():
    GPIO.output(Light, GPIO.HIGH)


class scheduler_motion:
    def __init__(self):

        p = os.fork()
        print(".....")
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(Host, Port, 300)

        with open("./motion/conf.json", "r", encoding="utf8") as fp:
            json_data = json.load(fp)
            print("获取json数据：", json_data)
        conf = json_data
        camera = PiCamera()
        camera.resolution = tuple(conf["resolution"])
        camera.framerate = conf["fps"]
        rawCapture = PiRGBArray(camera, size=tuple(conf["resolution"]))

        print("[INFO] Picamera Is Waking Up......")
        time.sleep(conf["camera_warmup_time"])

        m = Motion(conf, camera, rawCapture)

        jobstores = {"default": MemoryJobStore()}

        executors = {"default": ThreadPoolExecutor(20), "processpool": ProcessPoolExecutor(10)}

        job_defaults = {"coalesce": False, "max_instances": 3}

        scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
        now = datetime.datetime.now()
        now = now + datetime.timedelta(seconds=10)
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        print("scheduler will start at", now)

        if p == 0:
            time.sleep(3)
            client.loop_forever()
            print("执行子进程, pid={} ppid={} p={}".format(os.getpid(), os.getppid(), p))
        else:
            time.sleep(1)
            scheduler.add_job(m.cameraMain(), id="Motion", trigger="date", run_date=now)
            print("执行主进程, pid={} ppid={} p={}".format(os.getpid(), os.getppid(), p))

        self.scheduler = scheduler

    def startMotion(self, client):
        print("startMotion")
        self.scheduler.resume_job(job_id="Motion")

    def stopMotion(self):
        print("stopMotion")
        self.scheduler.pause_job(job_id="Motion")

    # Subscribe topic respberry
    def on_connect(self, client, userdata, flags, rc):
        client.subscribe("respberry")

    # Listen to news about subscribed topic respberry
    def on_message(self, client, userdata, msg):
        print(userdata)
        signal = msg.payload.decode("utf-8")
        print("\nGet The Infomation!:" + signal)
        if signal == "1":
            openLight()
        elif signal == "2":
            closeLight()
        elif signal == "3":
            self.startMotion(client)
        elif signal == "4":
            self.stopMotion()
        elif signal == "5":
            pass


print("emqx.ranzhendong.com.cn ready to connect ! ")
sm = scheduler_motion()
sm.scheduler.add_job(closeLight, id="Motions")
print(sm.scheduler)
sm.scheduler.start()
print(sm.scheduler.get_jobs())
sm.scheduler.pause_job(job_id="Motion")

# client.publish("emqtt", payload="Hello World", qos=0)
