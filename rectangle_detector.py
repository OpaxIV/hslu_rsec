#
# First Steps in Programming a Humanoid AI Robot
#
# Ball detector class
# Used by example_2_detect_ball.py
#

# Import required modules
import numpy as np
import cv2
import imutils

class RectangleDetector:
     
    # Class constructor
    def __init__(self):
        # Lower and upper limits for color
        # This example tracks green squares.
        # Also remember that OpenCVs hue range is scaled to 0..179
      
            self.colorLower = ( 30,  80,  80)
            self.colorUpper = ( 90, 255, 255)

    # Class method that detects a ball and marks it on the frame
    def detect(self, frame):
        # Convert frame from RGB to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        # Apply a bilateral filter to remove unwanted noise while preserving edges
        # For details on bilateral filtering, see
        hsv = cv2.bilateralFilter(hsv, 15, 100, 100)

        # Create a mask from the frame that only contains values falling in between colorLower...colorUpper
        mask = cv2.inRange(hsv, self.colorLower, self.colorUpper)

        # Apply some more filters to get rid of noise
        
        mask = cv2.erode(mask, None, iterations=3)
        mask = cv2.dilate(mask, None, iterations=2)

        # don't show window
        #cv2.imshow("Filter", mask)

        # Ask OpenCV to find all contours in the mask, then use IMutils' grab_contours() function
        # to extract all contours in a uniform format (independent of OpenCV library version).
       
        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # Find rectangle
        #rectangles = []
        max_area = 0
        center = None
        for cnt in cnts:
            # Calculate the area of the contour
            contour_area = cv2.contourArea(cnt)

            # Get the minimum enclosing rectangle and compute its area
            rect = cv2.minAreaRect(cnt) #
            ((x, y), (width,height), angleOfRotation)=rect
            rectangle_area = width * height
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(frame,[box],0,(0,0,255),2)

            # Ignore very small circles
            if width < 5 or height < 5:
               continue

            # If the area of the contour makes up for least 75% of the enclosing rectangle,
            # then the contour resembles a circle and we include it
            if contour_area / rectangle_area > 0.75:
                center = (int(x), int(y))
                #rectangles.append((center, int(rectangle_area)))
            """
                # Did we find a new biggest circle?
                if rectangle_area > max_area:
                    max_area = rectangle_area
                    max_center = center
            """

        
        # Return frame and center of largest circle
        return [frame, center]
