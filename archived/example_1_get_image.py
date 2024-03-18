#!/usr/bin/env python3
#
# First Steps in Programming a Humanoid AI Robot
#
# Shows a live image from Gretchen's camera.
# Press a key to exit program (with camera window focused)
#

# Import required modules
import cv2
import sys
sys.path.append('..')
from lib.ros_environment import ROSEnvironment
from lib.camera_v2 import Camera
import imutils
import numpy as np


def main():
    # Initalize ROS environment for connection to robot & camera
    ROSEnvironment()

    # Initialize & start camera
    camera = Camera()
    camera.start()
    
    bgsb_model = cv2.bgsegm.createBackgroundSubtractorMOG(history=500, nmixtures=3, backgroundRatio=0.7, noiseSigma=0)
    cv2.namedWindow('Frame')
    cv2.namedWindow('Foreground Mask')
    # Loop
    while True:
        # Get image from camera
        img = camera.getImage()
        
        # Use OpenCV to show image in a window named "Frame"
        # Note: imshow() expects the image to be in BRG format, 
        #       whereas camera.getImage() returns images in RBG 
        #       format. The [...,::-1] uses Python's array slicing
        #       capabilities to reverse the innermost dimension
        #       of the array from (r,g,b) to (b,g,r)
        
        # Our operations on the frame come here
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        fg_mask= bgsb_model.apply(img, learningRate=0.001)
        fg_mask = cv2.erode(fg_mask, None, iterations=10)
        fg_mask = cv2.dilate(fg_mask, None, iterations=10)
        #fg_mask = cv2.erode(fg_mask, None, iterations=3)

        # Display the resulting frame
        #Finds blobs in the foreground mask. We used findcontours and grab_contours before in https://teaching.csap.snu.ac.kr/gretchen-ai/isp22-gretchen-ai/-/blob/main/handson/05.BallTracking.md. Details can be found in https://www.educba.com/opencv-findcontours/
        cnts = cv2.findContours(fg_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        #Creates bounding boxes around blobs
        for cnt in cnts:
            cnt_area = cv2.contourArea(cnt)
            if(cnt_area > 200):
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                


        #shows the original image and foreground mask
        cv2.imshow("Frame", img[...,::-1])
        cv2.imshow("Foreground Mask", fg_mask[...,::1])


        # Exit loop if key was pressed
        key = cv2.waitKey(1)
        if key > 0:
            break


#
# Program entry point when started directly
#
if __name__ == '__main__':
    main()
