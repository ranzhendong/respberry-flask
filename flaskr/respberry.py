#!/usr/bin/env python3

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

# flask
app = Flask(__name__)
app.config.from_object("config")


@app.route("/")
def hello_world():
    return "Hello, World!"


# Set the pin to low level
def opens():
    GPIO.output(Light, GPIO.LOW)


# Set the pin to high level
def close():
    GPIO.output(Light, GPIO.HIGH)


# Subscribe topic respberry
def on_connect(client, userdata, flags, rc):
    client.subscribe("respberry")


# Listen to news about subscribed topic respberry
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
