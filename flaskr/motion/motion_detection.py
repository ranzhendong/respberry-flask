#!/usr/bin/env python3

from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import warnings
import datetime
import imutils
import json
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
        help="path to the JSON configuration file")
args = vars(ap.parse_args())
conf = json.load(open(args["conf"]))

camera = PiCamera()
camera.resolution = tuple(conf["resolution"])
camera.framerate = conf["fps"]
rawCapture = PiRGBArray(camera, size=tuple(conf["resolution"]))

print ("[INFO] Picamera Is Waking Up......")
time.sleep(conf["camera_warmup_time"])
avg = None
lastUploaded = datetime.datetime.now()
motionCounter = 0

second = time.time()
tuple_time = time.localtime(second)
time_zone = time.strftime("%Y-%m-%d_%H-%M-%S",tuple_time)

for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        second = time.time()
        tuple_time = time.localtime(second)
        time_zone = time.strftime("%Y-%m-%d_%H-%M-%S",tuple_time)

        frame = f.array
        timestamp = datetime.datetime.now()
        text = "NoMotion"

        frame = imutils.resize(frame, conf['tele_width'])
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if avg is None:
                print ("[INFO] Starting Background Modeling......")
                avg = gray.copy().astype("float")
                rawCapture.truncate(0)
                continue

        cv2.accumulateWeighted(gray, avg, 0.5)
        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

        thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
                cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
                if cv2.contourArea(c) < conf["min_area"]:
                        continue

                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
                text = "GetMotion"

        ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
        cv2.putText(frame, "LePai Regional Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.35, (0, 0, 255), 1)

        if text == "GetMotion":
                if (timestamp - lastUploaded).seconds >= conf["min_upload_seconds"]:
                        motionCounter += 1
                        if motionCounter >= conf["min_motion_frames"]:

                                cv2.imwrite('/root/graduation_design/warning/Motion/picture/warining_%s.png'%time_zone,frame )
                                print ('咦。。。好像有人哎。。。')
                                lastUploaded = timestamp
                                motionCounter = 0
        else:
                motionCounter = 0
        rawCapture.truncate(0)