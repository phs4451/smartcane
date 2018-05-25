# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO      # gpio ?�이브러�?from time import sleep       # sleep ?�이브러�?
#from time import sleep
import time
'''
VIB1 = 23
VIB2 = 25

GPIO.setmode(GPIO.BCM)      # GPIO 모드 ?�팅
GPIO.setup(VIB1,GPIO.OUT)
GPIO.setup(VIB2,GPIO.OUT)
'''
def setup(VIB1,VIB2):
    pwm_vib1 = GPIO.PWM(VIB1, 500)
    pwm_vib1.start(0)
    pwm_vib2 = GPIO.PWM(VIB2, 500)
    pwm_vib2.start(0)

def main(warning,pin_vib1, pin_vib2):
    
    if len(warning)==0:
        return
        
    elif len(warning) ==1:
        if 1 in warning:
            vibrate(True,False,1,pin_vib1, pin_vib2)
        elif 2 in warning:
            vibrate(True,True,1,pin_vib1, pin_vib2)
        elif 3 in warning:
            vibrate(False,True,1,pin_vib1, pin_vib2)
            
    elif len(warning)==2:
        if 1 and 2 in warning:
            vibrate(True,False,2,pin_vib1, pin_vib2)
        elif 2 and 3 in warning:
            vibrate(False,True,2,pin_vib1, pin_vib2)

    elif len(warning)==3:
        vibrate(True, True, 2, pin_vib1, pin_vib2)  
    
def clean_GPIO():
    pwm_vib1.stop()
    pwm_vib2.stop()
    GPIO.cleanup()
    
    
def vibrate (Left,Right,Type,pin_vib1, pin_vib2):
    setup(pin_vib1, pin_vib2)
    startime = time.time()
    
    High = 100
    Low = 0
    timeterm = 0.5
    runningtime = 5
    
    while True:
        if Type==1:
            if Left and Right:
                pwm_vib1.ChangeDutyCycle(High)
                pwm_vib2.ChangeDutyCycle(High)
                time.sleep(timeterm)
                pwm_vib1.ChangeDutyCycle(Low)
                pwm_vib2.ChangeDutyCycle(Low)
                time.sleep(timeterm)
        
                endtime = time.time()
                if endtime - starttime >=runningtime :
                    clean_GPIO()
                    break
            
            elif Left and (not Right):
                pwm_vib1.ChangeDutyCycle(High)
                time.sleep(timeterm)
                pwm_vib1.ChangeDutyCycle(Low)
                time.sleep(timeterm)
        
                endtime = time.time()
                if endtime - starttime >=runningtime :
                    clean_GPIO()
                    break
                    
            elif (not Left) and Right:
                pwm_vib2.ChangeDutyCycle(High)
                time.sleep(timeterm)
                pwm_vib2.ChangeDutyCycle(Low)
                time.sleep(timeterm)
        
                endtime = time.time()
                if endtime - starttime >= runningtime :
                    clean_GPIO()
                    break
                    
        elif Type==2:
            if Left and Right:
                pwm_vib1.ChangeDutyCycle(High)
                pwm_vib2.ChangeDutyCycle(High)
                endtime = time.time()
                if endtime - starttime >=runningtime :
                    clean_GPIO()
                    break
            elif Left and (not Right):
                pwm_vib1.ChangeDutyCycle(High)
                pwm_vib2.ChangeDutyCycle(Low)
                endtime = time.time()
                if endtime - starttime >= runningtime :
                    clean_GPIO()
                    break
            elif (not Left) and Right:
                pwm_vib1.ChangeDutyCycle(Low)
                pwm_vib2.ChangeDutyCycle(High)
                endtime = time.time()
                if endtime - starttime >=runningtime :
                    clean_GPIO()
                    break

def vibrate2(index,pin_vib1, pin_vib2):
    setup(pin_vib1, pin_vib2)
    starttime = time.time():
    
    High = 100
    timeterm = 0.5
    
    while True:
        if index ==1:
            pwm_vib1.ChangeDutyCycle(High)
            time.sleep(timeterm)
            clean_GPIO()
            break
        elif index ==2:
            pwm_vib1.ChangeDutyCycle(High)
            pwm_vib2.ChangeDutyCycle(High)
            time.sleep(timeterm)
            clean_GPIO()
            break
        elif index ==3:
            pwm_vib2.ChangeDutyCycle(High)
            time.sleep(timeterm)
            clean_GPIO()
            break
        else:
            clean_GPIO()
            break
'''
try:
    starttime = time.time()
    while True:
        duty_str = input("Enter Brightness (0 to 100):") 
        duty = int(duty_str)
        
        if duty > 100: 
            print("wrong input value.") 
        else: 
            pwm_vib.ChangeDutyCycle(duty) 
        
        endtime = time.time()
        if endtime-starttime >=5:
          break
                   
        end_key = raw_input(" - Stop to Blink LED, Please enter the 'end' : ") 
        if end_key == "end": 
          break
             
except KeyboardInterrupt:      # CTRL-C�??�르�?발생
        GPIO.cleanup()
'''        
        
if __name__ == '__main__':
   main()