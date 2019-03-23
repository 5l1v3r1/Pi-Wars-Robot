import cv2
import numpy as np
import RPi.GPIO as io 
from AMSpi import AMSpi

cam = cv2.VideoCapture(0)
 
with AMSpi() as amspi:
    while True:
        ret, orig_frame = cam.read()
        if not ret:
            cam = cv2.VideoCapture(0)
            continue
        frame = cv2.GaussianBlur(orig_frame, (5, 5), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        low_yellow = np.array([18, 94, 140])
        up_yellow = np.array([48, 255, 255])
        mask = cv2.inRange(hsv, low_yellow, up_yellow)
        edges = cv2.Canny(mask, 75, 150)
 
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=50)
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
                if (280 < x > 320):
                    amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4],speed=60) # ilerle
                else if ( 280 < x ):
                    amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_3]) # saga don
                    amspi.run_dc_motors([amspi.DC_Motor_2, amspi.DC_Motor_4], clockwise=False)

                else if (320<< x):
                    amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_3], clockwise=False)
                    amspi.run_dc_motors([amspi.DC_Motor_2, amspi.DC_Motor_4])

    cam.release()
    cv2.destroyAllWindows()