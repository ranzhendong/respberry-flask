#!/usr/bin/env python3

from flask import Flask
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

app = Flask(__name__)
app.config.from_object("config")

@app.route('/')
def hello_world():
    return 'Hello, World!'

Host = "emqx.ranzhendong.com.cn"
Port = 1883
bedroom = 35
ch = 26
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(bedroom, GPIO.OUT)
GPIO.setup(ch, GPIO.OUT)

def opens():
    print('|      Open Light !      |')
    print('+------------------------+')
    GPIO.output(ch, GPIO.LOW)

def close():
    print('|      Down Light !      |')
    print('+------------------------+')
    GPIO.output(ch, GPIO.HIGH)

def on_connect(client, userdata, flags, rc):
    print("emqx.eguagua.cn Connected with result code "+str(rc))
    client.subscribe("zhendong")

def on_message(client, userdata, msg):
    code = msg.payload.decode('utf-8')
    print("\nGet The Infomation!:\n+------------------------+")
    if code == '开灯':
        opens()
    elif  code == '关灯':
        close()

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(Host, Port, 300)
    client.loop_forever()