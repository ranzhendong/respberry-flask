#!/usr/bin/env python3

from flask import Flask
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

Host = "emqx.ranzhendong.com.cn"
Port = 1883
Light = 35
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(Light, GPIO.OUT)

app = Flask(__name__)
app.config.from_object("config")


@app.route("/")
def hello_world():
    return "Hello, World!"


def opens():
    GPIO.output(Light, GPIO.LOW)


def close():
    GPIO.output(Light, GPIO.HIGH)


def on_connect(client, userdata, flags, rc):
    client.subscribe("respberry")


def on_message(client, userdata, msg):
    code = msg.payload.decode("utf-8")
    print("\nGet The Infomation!:" + code)
    if code == "1":
        opens()
    elif code == "2":
        close()


print("emqx.ranzhendong.com.cn ready to connect ! ")
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(Host, Port, 300)
client.loop_forever()
