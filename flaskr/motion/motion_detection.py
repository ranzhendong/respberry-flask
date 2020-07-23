#!/usr/bin/env python3
import oss2
import requests
import urllib3
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import datetime
import imutils
import json
import time
import cv2


class Motion:
    def __init__(self, conf, camera, rawCapture):
        self.conf = conf
        self.camera = camera
        self.rawCapture = rawCapture
        self.time_zone = None
        self.scheduler_id = "Motion"

    def ding(self, Subject, Content):
        urllib3.disable_warnings()
        # requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        Url = "https://oapi.dingtalk.com/robot/send?access_token=788c2914731c64911b887d3f2b583d68ce6f9a5d0d6d2daa4a404e4d88ed3c1f"

        Header = {"Content-Type": "application/json", "Charset": "UTF-8"}

        Data = {
            "msgtype": "markdown",
            "markdown": {"title": Subject, "text": Content,},
        }
        r = requests.post(url=Url, data=json.dumps(Data), headers=Header, verify=False)
        return r.text

    def cameraMain(self):
        avg = None
        motionCounter = 0
        lastUploaded = datetime.datetime.now()
        conf = self.conf
        camera = self.camera
        rawCapture = self.rawCapture
        picture_path = conf["picture_path"]
        for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

            second = time.time()
            tuple_time = time.localtime(second)
            time_zone = time.strftime("%Y-%m-%d_%H-%M-%S", tuple_time)

            frame = f.array
            timestamp = datetime.datetime.now()
            text = "NoMotion"

            frame = imutils.resize(frame, conf["tele_width"])
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            if avg is None:
                print("[INFO] Starting Background Modeling......")
                avg = gray.copy().astype("float")
                rawCapture.truncate(0)
                continue

            cv2.accumulateWeighted(gray, avg, 0.5)
            frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

            thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for c in cnts:
                if cv2.contourArea(c) < conf["min_area"]:
                    continue

                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
                text = "GetMotion"

            ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
            cv2.putText(
                frame,
                "ShuLiData Regional Status: {}".format(text),
                (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                2,
            )
            cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

            if text == "GetMotion":
                if (timestamp - lastUploaded).seconds >= conf["min_upload_seconds"]:
                    motionCounter += 1
                    if motionCounter >= conf["min_motion_frames"]:
                        ts = "warining_%s.png" % time_zone
                        picture = picture_path + ts
                        cv2.imwrite(picture, frame)
                        print("咦。。。好像有人哎。。。")
                        lastUploaded = timestamp
                        motionCounter = 0
                        self.time_zone = time_zone
                        auth = oss2.Auth("LTAI4GHxymRvbWRDgWhFz8jy", "d2wJq9d01S2LDS1KN9rzxqBpsNiRMl")
                        # Endpoint以杭州为例，其它Region请按实际情况填写。
                        osshost = "http://oss-cn-hangzhou.aliyuncs.com"
                        bucket = oss2.Bucket(auth, osshost, "cv2raspberry")
                        bucket.put_object_from_file(ts, picture)
                        time.sleep(4)
                        p = osshost + "/" + ts
                        Subject = "OpenCV Notice！"
                        self.ding(Subject, Content="#### OpenCV Notice \n > ![screenshot](%s)" % p)
            else:
                motionCounter = 0
            rawCapture.truncate(0)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--conf", required=True, help="path to the JSON configuration file")
    args = vars(ap.parse_args())
    conf = json.load(open(args["conf"]))

    camera = PiCamera()
    camera.resolution = tuple(conf["resolution"])
    camera.framerate = conf["fps"]
    rawCapture = PiRGBArray(camera, size=tuple(conf["resolution"]))

    print("[INFO] Picamera Is Waking Up......")
    time.sleep(conf["camera_warmup_time"])
    m = Motion(conf, camera, rawCapture)
    m.cameraMain()
