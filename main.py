import warnings
import cv2
from matplotlib.pyplot import connect
import numpy as np
from PIL import Image, ImageGrab
from time import sleep
import controls
from lane_detection import LaneDetection
from steering_wheel import SteeringWheel

wheel = SteeringWheel()
lane = LaneDetection()


sleep(4)
last_lane = []
class_names = ['vleft', 'left', 'center', 'right', 'vright']
cur_steering = 0
counter = 10
while True:
    img = ImageGrab.grab(bbox=(0,40,1440,940))

    text = lane.get_steering_by_image(img, draw=True)
    targ_steer = class_names.index(text)
    while targ_steer != cur_steering:
        if targ_steer < cur_steering:
            controls.left()
            cur_steering -= 1
        elif targ_steer > cur_steering: 
            controls.right()
            cur_steering += 1
    if counter == 20:
        counter = 0
        res = wheel.get(img)
        #print(res)
        cur_steering = class_names.index(res)
        #print(f'mean {targ_steer} real {cur_steering}')
    counter += 1