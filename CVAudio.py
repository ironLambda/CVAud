from collections import deque
import numpy as np
import argparse
import imutils
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import PicAud as p
import pyaudio
from threading import Thread
from queue import Queue 

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
                help="max buffer size")
ap.add_argument("-i", "--image", help="Path to an image file")
args = vars(ap.parse_args())

# Define the Color range we are tracking
greenLower = (12, 83, 0)
greenUpper = (42, 255, 255)

# Set up variables
pts = deque(maxlen=args["buffer"])
counter = 0
pyaud = pyaudio.PyAudio()
stream = pyaud.open(format=pyaudio.paInt16, channels=1, rate=4000, output=True)
waves = Queue()


def playthread(waves):
    
    for wave in iter(waves.get, None):
        
        print(wave)
        stream.write(wave.astype(np.int8))
        
    
        
thread = Thread( target=playthread, args=(waves,))
thread.start()

# run image program if flag used
if args.get("image", False):
    p.picToAud(cv2.imread(args["image"]))
    exit(0)

# If video supplied, use video, otherwise use webcam
if not args.get("video", False):
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 60
    raw = PiRGBArray(camera, size=(640, 480))
    time.sleep(0.1)
else:
    camera = cv2.VideoCapture(args["video"])

n = 0
v = 0
    
for rawim in camera.capture_continuous(raw, format="bgr", use_video_port = True):

    # make frame smaller, in the right direction, and in the right color space
    frame = rawim.array
    cv2.flip(frame, 1, frame)
    blur = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Highlight the green objects
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # select the green object
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    

    # Draw circle around object
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)

        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
        n, v = center

        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            pts.appendleft(center)

    # figure out movement direction
    wave = p.genWaveRealtime([v, n])
    stream.write(wave.astype(np.int8))
    
    cv2.imshow("Frame",frame)
    key = cv2.waitKey(1) & 0xFF
    counter += 1

    if key == ord("q"):
        break
    raw.truncate(0)
    


# Cleanup
camera.release()
cv2.destroyAllWindows()
