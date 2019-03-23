import time 
import RPi.GPIO as io 
from AMSpi import AMSpi

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 24
ECHO = 23

TRIG2 = 10
ECHO2 = 9

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.setup(TRIG2,GPIO.OUT)
GPIO.setup(ECHO2,GPIO.IN)

io.setmode(io.BCM)
proximity = 14
io.setup(proximity, io.IN) # activate input 

with AMSpi() as amspi:
    amspi.set_74HC595_pins(21, 20, 16)

    amspi.set_L293D_pins(5, 6, 13, 19)

    while(True):
            GPIO.output(TRIG, False)
            GPIO.output(TRIG2, False)
            time.sleep(2)
            GPIO.output(TRIG, True)
            GPIO.output(TRIG2, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)
            GPIO.output(TRIG2, False)
            while GPIO.input(ECHO)==0:
                pulse_start = time.time()
            while GPIO.input(ECHO)==1:
                pulse_end = time.time()
                pulse_duration = pulse_end - pulse_start
                distance = pulse_duration * 17150
                distance = round(distance, 2)


            while GPIO.input(ECHO2)==0:
                pulse_start2 = time.time()
            while GPIO.input(ECHO2)==1:
                pulse_end2 = time.time()
                pulse_duration2 = pulse_end2 - pulse_start2
                distance2 = pulse_duration2 * 17150
                distance2 = round(distance2, 2)
        if(distance > 10): # sag tarafta bosluk varsa saga don
            amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_4])
            amspi.run_dc_motors([amspi.DC_Motor_3, amspi.DC_Motor_2], clockwise=False)
            time.sleep(1)
        else if (distance2 > 10) # sol tarafta bosluk varsa sola don
            amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_3], clockwise=False)
            amspi.run_dc_motors([amspi.DC_Motor_2, amspi.DC_Motor_4])
            time.sleep(1)

        if io.input(proximity):
            print("Engel Yok")
            amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4],speed=100)
        else:
            print("Engel Algilandi")
            amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_4]) # sola don
            amspi.run_dc_motors([amspi.DC_Motor_3, amspi.DC_Motor_2], clockwise=False)
            time.sleep(1)