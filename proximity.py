import time 
import RPi.GPIO as io 
from AMSpi import AMSpi

io.setmode(io.BCM) 

proximity = 14
io.setup(proximity, io.IN) # activate input 

with AMSpi() as amspi:

    amspi.set_74HC595_pins(21, 20, 16)
    
    amspi.set_L293D_pins(5, 6, 13, 19)
    while(True):
    	if io.input(proximity):
    		print("Engel Yok")
    		amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4],speed=100)
    	else:
    		print("Engel Algılandı")
    		amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])