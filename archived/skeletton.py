#!/usr/bin/env python3
#
# First Steps in Programming a Humanoid AI Robot
#
# Short program description.
# 


# Import required modules
import cv2
import sys
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.robot import Robot
from lib.ros_environment import ROSEnvironment


# Create camera & robot
camera = Camera()
robot = Robot()


# Method executed on click in camera image
def onMouse(event, u, v, flags, param):
    # If left button is clicked...
    if event == cv2.EVENT_LBUTTONDOWN:
        # Do something


def main():
    # Initalize ROS environment, start robot and camera
    ROSEnvironment()
    robot.start()
    camera.start()

    # Create a window called "Frame" and install a mouse handler
    cv2.namedWindow("Frame")
    cv2.setMouseCallback("Frame", onMouse)

    # Loop
    while True:
        # Get image from camera
        img = camera.getImage()

        # Do something

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

