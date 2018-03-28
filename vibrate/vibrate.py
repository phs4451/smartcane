# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO      # gpio ?�이브러�?from time import sleep       # sleep ?�이브러�?
from time import sleep

VIB = 22

GPIO.setmode(GPIO.BCM)      # GPIO 모드 ?�팅
GPIO.setup(VIB,GPIO.OUT)

pwm_vib = GPIO.PWM(VIB, 500)
pwm_vib.start(100)

print 'Start the GPIO App'  # ?�작???�리??
print "Press the button (CTRL-C to exit)"
try:
    while True:
        duty_str = input("Enter Brightness (0 to 100):") 
        duty = int(duty_str)
        
        if duty > 100: 
            print("wrong input value.") 
        else: 
            pwm_vib.ChangeDutyCycle(duty) 
            
        end_key = raw_input(" - Stop to Blink LED, Please enter the 'end' : ") 
        if end_key == "end": 
          break

       
        
except KeyboardInterrupt:      # CTRL-C�??�르�?발생
        GPIO.cleanup()
