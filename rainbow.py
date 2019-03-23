import cv2
import numpy as np
import RPi.GPIO as io 
from AMSpi import AMSpi

durum = 1
io.setmode(io.BCM) 
proximity = 14
io.setup(proximity, io.IN) 

cap = cv2.VideoCapture(0)
with AMSpi() as amspi:
    
    amspi.set_74HC595_pins(21, 20, 16) # motor pinleri
    amspi.set_L293D_pins(5, 6, 13, 19)

    while(1):
        _, img = cap.read()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #  kırmızı
        red_lower = np.array([136,87,111],np.uint8)
        red_upper = np.array([180,255,255],np.uint8)
         # mavi
        blue_lower = np.array([99,115,150],np.uint8)
        blue_upper = np.array([110,255,255],np.uint8)
         # sari
        yellow_lower = np.array([22,60,200],np.uint8)
        yellow_upper = np.array([60,255,255],np.uint8)
        # Yesil
        green_lower = np.array([65,60,60], np.uint8)
        green_upper = np.array([80,255,255],np.uint8)
        
        red = cv2.inRange(hsv, red_lower, red_upper)
        blue = cv2.inRange(hsv, blue_lower, blue_upper)
        yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
        green = cv2.inRange(hsv, green_lower, green_upper)
        
        kernal = np.ones((5, 5), "uint8")

        red = cv2.dilate(red, kernal)
        res_red = cv2.bitwise_and(img, img, mask = red)

        blue = cv2.dilate(blue, kernal)
        res_blue = cv2.bitwise_and(img, img, mask = blue)
        
        yellow = cv2.dilate(yellow, kernal)
        res_yellow = cv2.bitwise_and(img, img, mask = yellow)

        green = cv2.dilate(green, kernal)
        res_green = cv2.bitwise_and(img, img, mask = green)
        # Tracking red
        (_, contours, hierarchy)=cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(img, "Red Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))  
                if (durum == 1): 
                    if (280 < x > 320): # renk kameranin ortasindaysa 
                            if io.input(proximity): #  uzaklik sensoru algilamadiysa
                                print("Renk Alaninda degilim")
                                amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4],speed=100) # sensor gorene kadar git
                            else:
                                print("Gorev Tamamlandi") # sensor algiladiysa hedefe ulasmis demektir
                                amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4], clockwise=False) # geri don
                                time.sleep(2)
                                durum = 2 # 2. renk'e gec
                    else:
                        amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_3]) # kendi etrafında don
                        amspi.run_dc_motors([amspi.DC_Motor_2, amspi.DC_Motor_4], clockwise=False)



        # Tracking blue
        (_, contours, hierarchy)=cv2.findContours(blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(img, "Blue Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0))
                if (durum == 2):
                    if (280 < x > 320):
                            if io.input(proximity):
                                print("Renk Alaninda degilim")
                                amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4],speed=100) # sensor gorene kadar git
                            else:
                                print("Gorev Tamamlandi")
                                amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4], clockwise=False) # geri don
                                time.sleep(2)
                                durum = 3
                    else:
                        amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_3]) # kendi etrafında don
                        amspi.run_dc_motors([amspi.DC_Motor_2, amspi.DC_Motor_4], clockwise=False)

        # Tracking yellow
        (_, contours, hierarchy)=cv2.findContours(yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, "Yellow Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))
                if (durum == 4):
                    if (280 < x > 320):
                            if io.input(proximity):
                                print("Renk Alaninda degilim")
                                amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4],speed=100) # sensor gorene kadar git
                            else:
                                print("Gorev Tamamlandi")
                                amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4], clockwise=False) # geri don
                                time.sleep(2)
                                durum = 5
                            else:
                        amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_3]) # kendi etrafında don
                        amspi.run_dc_motors([amspi.DC_Motor_2, amspi.DC_Motor_4], clockwise=False)

        (_, contours, hierarchy)=cv2.findContours(green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, "Green Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))
                if (durum == 3):
                    if (280 < x > 320):
                            if io.input(proximity):
                                print("Renk Alaninda degilim")
                                amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4],speed=100) # sensor gorene kadar git
                            else:
                                print("Gorev Tamamlandi")
                                amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4], clockwise=False) # geri don
                                time.sleep(2)
                                durum = 4
                    else:
                        amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_3]) # kendi etrafında don
                        amspi.run_dc_motors([amspi.DC_Motor_2, amspi.DC_Motor_4], clockwise=False)
        if (durum == 5):
            amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4]) # motorları durdur


    cap.release()
    cv2.destroyAllWindows()