#!/usr/bin/env python3
import os
import sys
import time

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler

# from picamera.array import PiRGBArray
# from picamera import PiCamera
from flask import Flask

# from flaskr.motion.motion_detection import Motion
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

# flask
app = Flask(__name__)
app.config.from_object("config")


@app.route("/")
def hello_world():
    return "Hello, World!"


# Set the pin to low level
def openLight():
    GPIO.output(Light, GPIO.LOW)


# Set the pin to high level
def closeLight():
    GPIO.output(Light, GPIO.HIGH)


class scheduler_motion:
    def __init__(self):
        conf = {}
        # camera = PiCamera()
        # camera.resolution = tuple(conf["resolution"])
        # camera.framerate = conf["fps"]
        # rawCapture = PiRGBArray(camera, size=tuple(conf["resolution"]))

        print("[INFO] Picamera Is Waking Up......")
        # time.sleep(conf["camera_warmup_time"])

        # m = Motion(conf, camera, rawCapture)
        # m = Motion(conf, "camera", "rawCapture")

        jobstores = {"default": MemoryJobStore()}

        executors = {"default": ThreadPoolExecutor(20), "processpool": ProcessPoolExecutor(10)}

        job_defaults = {"coalesce": False, "max_instances": 3}

        scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
        # scheduler.add_job(m.cameraMain(), "interval", minutes=2, id="Motion")
        scheduler.add_job(closeLight, id="Motion")

        self.scheduler = scheduler

    def startMotion(self):
        self.scheduler.resume_job(job_id="Motion")

    def stopMotion(self):
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
            self.startMotion()
        elif signal == "4":
            self.stopMotion()
        elif signal == "5":
            pass


print("emqx.ranzhendong.com.cn ready to connect ! ")
sm = scheduler_motion()
sm.scheduler.add_job(closeLight, id="Motions")
client = mqtt.Client()
print(sm.scheduler)
sm.scheduler.start()
print(sm.scheduler.get_jobs())
sm.scheduler.pause_job(job_id="Motion")

client.on_connect = sm.on_connect
client.on_message = sm.on_message
client.connect(Host, Port, 300)
client.loop_forever()

# client.publish("emqtt", payload="Hello World", qos=0)
