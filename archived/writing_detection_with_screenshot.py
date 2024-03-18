#!/usr/bin/env python3
#
# Note: The video image and the canvas are both arrays! both are np arrays!


### THIS IMPLEMENTATION IS NOT WORKING ###

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
import time

## Initiliaze Gobals
camera_port = 0
camera = cv2.VideoCapture(camera_port)

robot = Robot()

rectangle_detector = RectangleDetector()

#red = (255, 0, 0) # unused, alternative color
black = (0,0,0)
circles = queue.LifoQueue()


def takeScreenshot(img_path):
    cv2.imwrite("screenshot.png",img_path)
    time.sleep(5)


def main():
    ROSEnvironment()
    
    robot.start()
    cv2.namedWindow("Frame")
    cv2.namedWindow("Frame2")

    # initialize canvas
    canvas = np.full((480, 640),1 , dtype="uint8") # size same as camera, 1 channel vs 3 channels
    merged_rbg = np.zeros((480, 640), dtype="uint8")

    # Loop
    while True:
        # Get image from camera
        img = camera.read()

        # Run ball detector on image, runs continuously and gets coordinates
        (img, center) = rectangle_detector.detect(img)
        
        # move camera if position is in the outer ~10% of the frame
        if center != None and (center[0]<64 or center[0]>576 or center[1]<48 or center[1]> 432): #if center outside of "inner area" move to look at center
             (x,y,z) = camera.convert2d_3d(center[0],center[1])
             (x,y,z) = camera.convert3d_3d(x,y,z)
             robot.lookatpoint(x,y,z, 2)



        if center != None:
            circles.put(center) # add centers to list
            cv2.circle(canvas, (center[0], center[1]), 5,0,-1)
            
            # fill white spaces inbetween dots
            # fill only if at least one point is in the queue
            if circles.qsize() > 1:
                p1 = circles.get()
                p2 = circles.get()
                cv2.line(canvas, p1, p2, 0, 15)
            
        r = img[:,:,0]
        g = img[:,:,1]
        b = img[:,:,2]

        r[canvas == 0] = black[0] # 0 corresponds to color black
        g[canvas == 0] = black[1]
        b[canvas == 0] = black[2]
        
        merged_rbg = cv2.merge([r,g,b])


        # Display image
        cv2.imshow("Frame", merged_rbg[..., ::-1])
        #cv2.imshow("Frame2", canvas[..., ::-1])
        
        if circles != None:
            takeScreenshot(img) # take a screenshot every 5 seconds
        

        # Exit loop if key was pressed (in frame)
        key = cv2.waitKey(1)
        if key > 0:
            break


#
# Program entry point when started directly
#
if __name__ == "__main__":
    main()  
