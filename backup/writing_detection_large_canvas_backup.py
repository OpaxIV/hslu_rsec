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
robot = Robot()


# Initalize ball detector
rectangle_detector = RectangleDetector()

# blue = (0, 0, 255)
# blue = (255, 0, 0)
#red = (255, 0, 0) # color red, color for circles
black = (0,0,0)
circles = queue.LifoQueue() # first in first out
#centers = queue.LifoQueue(1) # first in first out



# canvas
canvas_maxx = 640
canvas_maxy = 480

# fov
fov_maxx = 1.0
fov_maxy = 0.6



def transform(x,y):
    # recieving coordinates in m * 100 -> cm * 10 -> pixel 
    x = (x*canvas_maxx/fov_maxx)+canvas_maxx/2
    y = (y*canvas_maxy/fov_maxy)+canvas_maxy/2
    return (x,y)


def main():
    ROSEnvironment()
    camera.start()
    robot.start()
    cv2.namedWindow("Frame")
    cv2.namedWindow("Canvas")
    currentFocus=(0,0,0)
    # initialize canvas
    canvas = np.full((canvas_maxy, canvas_maxx),255, dtype="uint8") # one layer instead of 3
    merged_rbg = np.zeros((480, 640), dtype="uint8")
    center = None
    # Loop
    while True:
        # Get image from camera
        img = camera.getImage()

        # Run ball detector on image, runs continously and gets coordinates
        (img, cen) = rectangle_detector.detect(img)
        

        # center can't be None
        #if center != None:
         #       centers.get()
          #      centers.put(center)
        if cen != None: 
             center=cen

        # move camera if position is in the outer ~10% of the frame
        if center != None and (center[0]<64 or center[0]>576 or center[1]<48 or center[1]> 432): #if center outside of "inner area" move to look at center
             (x,y,z) = camera.convert2d_3d(center[0],center[1])
             (x,y,z) = camera.convert3d_3d(x,y,z)
             currentFocus = (x,y,z)
             robot.lookatpoint(x,y,z, 2)

        #because the coordinates (x,y,z) are absolute (=> the robot's coordinate system) uses those to draw
        #print(center)

        if center != None:
            (x,y,z) = camera.convert2d_3d(center[0],center[1])
            (robot_z,robot_y,robot_x) = camera.convert3d_3d(x,y,z)
            print((robot_x,robot_y,robot_z))
            (x,y) = transform(robot_x,robot_y)
            print((x,y))
            circles.put((x,y)) # add centers to list
            cv2.circle(canvas, (int(x), int(y)), 5,0,-1)
            
            if circles.qsize() > 1:
                p1 = circles.get()
                p2 = circles.get()
                cv2.line(canvas, (int(p1[0]),int(p1[1])), (int(p2[0]), int(p2[1])), 0, 15)
            

        r = img[:,:,0]
        g = img[:,:,1]
        b = img[:,:,2]

        # only check for the points in the camera focus
        # used to draw on camera
        (xView, yView) = transform(currentFocus[0],currentFocus[1])
        #view_of_canvas = canvas[(xView-240),(xView+240)][(yView-320),(yView+320)]
        """ r[view_of_canvas == 0] = black[0] # value corresponds to circle value 255 (white)
        g[view_of_canvas == 0] = black[1]
        b[view_of_canvas == 0] = black[2]
         """
        merged_rbg = cv2.merge([r,g,b])

        


            # Display image
        cv2.imshow("Frame", merged_rbg[..., ::-1])
        #cv2.imshow("Frame2", canvas[..., ::-1])
            
        # show canvas
        cv2.imshow("Canvas", canvas[..., ::-1])

        # Exit loop if key was pressed (in frame)
        key = cv2.waitKey(1)
        if key > 0:
            break





#
# Program entry point when started directly
#
if __name__ == "__main__":
    main()  
