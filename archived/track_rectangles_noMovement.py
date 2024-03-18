#!/usr/bin/env python3
#
# First Steps in Programming a Humanoid AI Robot
#
# Detect and track a ball
# Press a key to exit program (with camera window focused)
#
# Currently, this exercise is a copy of example 2. Modify it such that
# * it allows the user to click on the image and select the color of the filter
# * it moves Gretchen's head to follow the largest detected rectangle.
#

# Import required modules
import cv2
import sys
from rectangle_detector import RectangleDetector
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.robot import Robot
from lib.ros_environment import ROSEnvironment


# Initalize ROS environment and camera
ROSEnvironment()
camera = Camera()
camera.start()
robot = Robot()
robot.start()

# Initalize ball detector
rectangle_detector = RectangleDetector()

def main():
    
    # Announce frame and set mouse handler
    cv2.namedWindow("Frame")
    

    # Loop
    while True:
        # Get image from camera
        img = camera.getImage()
	
        # Run ball detector on image
        (img, center) = rectangle_detector.detect(img)
              
        
        # Display image
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
