#!/usr/bin/env python3
#
# Gretchen Drawing Detector
#
# Authors:
#   Andriy Popov
#   Fabio Schmidt
#   Myriam Eschenlohr


# Notes:
#   - The video image and the canvas are both arrays! both are np arrays!
#   - frameWidth = 640  & frameHeight = 480 = aspect ratio of camera view




# Import required modules
import cv2
import sys
from rectangle_detector import RectangleDetector 
import numpy as np
sys.path.append("..")
from lib.camera_v2 import Camera
from lib.ros_environment import ROSEnvironment
from lib.robot import Robot

# Initiliaze Camera and Motors
camera = Camera()
robot = Robot()

# Initalize ball detector
rectangle_detector = RectangleDetector()

# Colors
# red = (255, 0, 0) # unused color, can be exchanged w/ black
black = (0,0,0)



# Canvas
canvas_maxx = 800   # 640 original aspect ratio
canvas_maxy = 600   # 480

# FOV
fov_maxx = 1.0
fov_maxy = 0.6


# Transformation function, applied to get "new" center coordinates when camera is moving
def transform(x,y): 
    x = (-1*(x*canvas_maxx/fov_maxx)+canvas_maxx/2)
    y = (-1*(y*canvas_maxy/fov_maxy)+canvas_maxy/2)
    return (x,y)


def main():
    ROSEnvironment()
    camera.start()
    robot.start()
    cv2.namedWindow("Frame")
    cv2.namedWindow("Canvas")
    currentFocus=(0,0,0)


    # Initialize canvas frame
    canvas = np.full((canvas_maxy, canvas_maxx),255, dtype="uint8") # one channel instead of 3
    # Initizialize image frame
    merged_rbg = np.zeros((480, 640), dtype="uint8")
    
    # Center is currently non existant (= none)
    center = None
    
    
    while True:
        # Get image from camera
        img = camera.getImage()

        # Run ball detector on image, runs continously and gets coordinates
        (img, cen) = rectangle_detector.detect(img)
        

        if cen != None: 
             center=cen


        # check drawing position, take camera movement/position into account
        if center != None and (center[0]>64 or center[0]<576 or center[1]>48 or center[1]<432): #if center outside of "inner area" move to look at center
            (x,y,z) = camera.convert2d_3d(center[0],center[1])
            (robot_z,robot_y,robot_x) = camera.convert3d_3d(x,y,z)
            (y,x) = transform(robot_x,robot_y)
            cv2.circle(canvas, (int(x), int(y)), 5,0,-1)
            

        # move camera if position is in the outer ~10% of the frame
        if center != None and (center[0]<64 or center[0]>576 or center[1]<48 or center[1]> 432):
             (x,y,z) = camera.convert2d_3d(center[0],center[1])
             (x,y,z) = camera.convert3d_3d(x,y,z)
             currentFocus = (x,y,z)
             robot.lookatpoint(x,y,z, 2)

        # "split" the three image channels and compare 
        r = img[:,:,0]
        g = img[:,:,1]
        b = img[:,:,2]

        # "merge" the image channels back together
        merged_rbg = cv2.merge([r,g,b])



        # Display image
        cv2.imshow("Frame", merged_rbg[..., ::-1])
            
        # Display canvas
        cv2.imshow("Canvas", canvas[..., ::1])

        # Exit loop if key was pressed (in frame)
        # takes a screenshot every time the program is closed (saves the scribble)
        key = cv2.waitKey(1)
        if key > 0:
            cv2.imwrite("screenshot.jpg",canvas)
            break


# Program entry point when started directly
if __name__ == "__main__":
    main()  
