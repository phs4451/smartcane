# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO      
import time
import math
 
def vibrate_top(pin_vib3):
    pwm_vib3 =GPIO.PWM(pin_vib3,1000)
    pwm_vib3.start(0)
    
    starttime = time.time()
    runningtime = 1.5
    High = 100
    timeterm1 = 0.5
    timeterm2 = 0.25
    try:
        while True:
            pwm_vib3.start(High)
            time.sleep(timeterm1)
            pwm_vib3.stop()
            time.sleep(timeterm2)
        
            endtime = time.time()
            if endtime-starttime >= runningtime:
                break
    finally:
        pwm_vib3.stop()
        print('vibrate stop')
    
def vibrate_bottom(index, pin_vib1, pin_vib2):
    time.sleep(0.05)
    pwm_vib1 = GPIO.PWM(pin_vib1, 1000)
    pwm_vib2 = GPIO.PWM(pin_vib2, 1000)
    pwm_vib1.start(0)
    pwm_vib2.start(0)
    High = 100
    timeterm = 0.3
    
    try:
        if index == 1:
            pwm_vib1.start(High)
            time.sleep(timeterm)
            pwm_vib1.stop()
            return
        elif index == 2:
            pwm_vib1.start(High)
            pwm_vib2.start(High)
            time.sleep(timeterm)
            pwm_vib1.stop()
            pwm_vib2.stop()
            return
        elif index == 3:
            pwm_vib2.start(High)
            time.sleep(timeterm)
            pwm_vib2.stop()
            return                
    finally:
        pwm_vib1.stop()
        pwm_vib2.stop()
        
if __name__ == '__main__':
   main()
