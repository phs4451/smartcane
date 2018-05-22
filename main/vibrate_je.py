# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO      # gpio ?¼ì´ë¸ŒëŸ¬ë¦?from time import sleep       # sleep ?¼ì´ë¸ŒëŸ¬ë¦?
#from time import sleep
import time
'''
VIB1 = 23
VIB2 = 25

GPIO.setmode(GPIO.BCM)      # GPIO ëª¨ë“œ ?‹íŒ…
GPIO.setup(VIB1,GPIO.OUT)
GPIO.setup(VIB2,GPIO.OUT)
'''

pwm_vib1 = GPIO.PWM(VIB1, 500)
pwm_vib1.start(100)
pwm_vib2 = GPIO.PWM(VIB2, 500)
pwm_vib2.start(100)

print 'Start the GPIO App'  # ?œì‘???Œë¦¬??
print "Press the button (CTRL-C to exit)"
def main(warning):
    if len(warning) ==1:
        if 1 in warning:
            vibrate(True,False,1)
        elif 2 in warning:
            vibrate(True,True,1)
        elif 3 in warning:
            vibrate(False,True,1)
            
    elif len(warning)>=2:
        if 1 and 2 in warning:
            vibrate(True,False,2)
        elif 2 and 3 in warning:
            vibrate(False,True,2)
        else:
            vibrate(True,True,2)   
    
    
    
def vibrate (Left,Right,Type):
    startime = time.time()
    while True:
        if Type==1:
            
            pwm_vib1.ChangeDutyCycle(100)
            time.sleep(0.5)
            pwm_vib1.ChangeDutyCycle(0)
            time.sleep(0.5)
        
            endtime = time.time()
            if endtime - starttime >=5:
                break
            
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
'''                    
        end_key = raw_input(" - Stop to Blink LED, Please enter the 'end' : ") 
        if end_key == "end": 
          break
'''
             
except KeyboardInterrupt:      # CTRL-Cë¥??„ë¥´ë©?ë°œìƒ
        GPIO.cleanup()
        
        
if __name__ == '__main__':
   main()