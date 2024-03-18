#!/usr/bin/env python3
#
# Note: The video image and the canvas are both arrays! both are np arrays!

# Import required modules
import cv2
import sys
from rectangle_detector import RectangleDetector
import numpy as np
sys.path.append("..")
from lib.camera_v2 import Camera
from lib.ros_environment import ROSEnvironment
from lib.robot import Robot
import queue

## Initiliaze Globals

# frameWidth = 640 size of camera
# frameHeight = 480 size of camera

camera = Camera()

# Initalize ball detector
ball_detector = RectangleDetector()

# blue = (0, 0, 255)
# blue = (255, 0, 0)
red = (255, 0, 0) # color red, color for circles

circles = queue.LifoQueue() # first in first out





def main():
    ROSEnvironment()
    camera.start()
    cv2.namedWindow("Frame")
    #lcv2.namedWindow("Frame2")

    # initialize canvas
    canvas = np.zeros((480, 640), dtype="uint8") # one layer instead of 3
    merged_rbg = np.zeros((480, 640), dtype="uint8")

    # Loop
    while True:
        # Get image from camera
        img = camera.getImage()

        # Run ball detector on image, runs continously and gets coordinates
        (img, center) = ball_detector.detect(img)
        

        if center != None:
            circles.put(center) # add centers to list
            cv2.circle(canvas, (center[0], center[1]), 5,255,-1)
            
            if circles.qsize() > 1:
                p1 = circles.get()
                p2 = circles.get()
                cv2.line(canvas, p1, p2, 255, 15)
            

        r = img[:,:,0]
        g = img[:,:,1]
        b = img[:,:,2]

        r[canvas == 255] = red[0] # value corresponds to circle value 255 (white)
        g[canvas == 255] = red[1]
        b[canvas == 255] = red[2]
        
        merged_rbg = cv2.merge([r,g,b])


            # Display image
        cv2.imshow("Frame", merged_rbg[..., ::-1])
            
            # show canvas
            #cv2.imshow("Frame", canvas[..., ::-1])

        # Exit loop if key was pressed (in frame)
        key = cv2.waitKey(1)
        if key > 0:
            break


#
# Program entry point when started directly
#
if __name__ == "__main__":
    main()  
