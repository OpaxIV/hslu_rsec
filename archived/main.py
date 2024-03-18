#!/usr/bin/env python3



# Import required modules
import cv2
import sys
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.robot import Robot
from lib.ros_environment import ROSEnvironment
import numpy as np
import math
import imutils


# Create camera & robot
camera = Camera()




def main():
    
    ROSEnvironment()
    camera.start()

    
    cv2.namedWindow("Frame")

    
    while True:
        # Get image from camera
        img = camera.getImage()

        cv2.rectangle(img, (300, 300), (100, 100), (0, 255, 0), 0) # draw rectangle around picture
        img_cropped = img[100:300, 100:300]
        grey = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2GRAY)
        blurred_ = cv2.GaussianBlur(grey, (35, 35), 0) # apply gaussian filter
        thresholded = cv2.threshold(blurred_, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) # image tresholding

    
         mask = cv2.erode(mask, kernel=None, iterations)
        mask = cv2.dilate(mask, kernel=None, iterations)

        # grab contours
        contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
    
    
        # Use OpenCV to show camera image the window named "Frame"
        cv2.imshow("Frame", img[...,::-1])

       
        
        
        # Exit loop if key was pressed
        key = cv2.waitKey(1)
        if key > 0:
            break


#
# Program entry point when started directly
#
if __name__ == '__main__':
    main()

