#!/usr/bin/env python3
#
# First Steps in Programming a Humanoid AI Robot
#
# Detect and track a ball
# Press a key to exit program (with camera window focused)
#
# Currently, this exercise is a copy of example 2. Modify it such that
# * it allows the user to click on the image and select the color of the filter
# * it moves Gretchen's head to follow the largest detected circle. - done
#

# Import required modules
import cv2
import sys
from ball_detector import BallDetector
import numpy as np

sys.path.append("..")
from lib.camera_v2 import Camera
from lib.ros_environment import ROSEnvironment
from lib.robot import Robot



## Initiliaze Globals
# Initalize ROS environment and camera
ROSEnvironment()
camera = Camera()
camera.start()

# Initalize ball detector
ball_detector = BallDetector()


saved_centers = list(set([])) # no duplicates



def main():
    # for mouse input
    # Announce frame and set mouse handler
    cv2.namedWindow("Frame")    



    # Loop
    while True:
        # Get image from camera
        img = camera.getImage()

        # Run ball detector on image
        (img, center) = ball_detector.detect(img)

        if center != None:
            
            ## FEHLER IST HIER, DIE KOORDINATEN SIND MÜLL
            # get coordinates of center and compute kinematics
            #(x, y, z) = camera.convert2d_3d(center[0], center[1]) # image frame -> object 
            #coordinates = camera.convert3d_3d(x, y, z)              # object -> robot
            saved_centers.append((center[0],center[1])) # save centers, of circles. will be drawn over later
            
            
            # for testing only
            #for i in saved_centers:
            #   print(i)


        # drawing
        # cv2.circle
            
        # initialize canvas 300x300, RGB black background
        #canvas = np.zeros((300, 300, 3), dtype="uint8") # empty array
        

        """ info = [ ( 1, 2), (3, 4), (5, 6) ]
        info[0][0] == 1         info[0][1] == 2
        info[1][0] == 3
        info[1][1] == 4
        info[2][0] == 5
        info[2][1] == 6
         """

        # blue = (0, 0, 255)
        # blue = (255, 0, 0)
        i = int(0)
        j = int(0)
        counter = int(0)
        for t in saved_centers:
                cv2.circle(img, (saved_centers[i][j],saved_centers[i][j+1]), 20, (255, 0, 0),-1)
                #print((saved_centers[i][j],saved_centers[i][j+1])) #--> draws every time, it works
                if counter % 2 == 0:
                     i += 1
                     j = 0
                counter += 1
                #print("i: " + str(i) + " j: " + str(j) + " counter " + str(counter))

        # Display image
        cv2.imshow("Frame", img[..., ::-1])

        # Exit loop if key was pressed (in frame)
        key = cv2.waitKey(1)
        if key > 0:
            break


#
# Program entry point when started directly
#
if __name__ == "__main__":
    main()
