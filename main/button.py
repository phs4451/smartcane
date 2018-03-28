# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO      # gpio ?¼ì´ë¸ŒëŸ¬ë¦?from time import sleep       # sleep ?¼ì´ë¸ŒëŸ¬ë¦?
from time import sleep

Button = 18
count = 0


GPIO.setmode(GPIO.BCM)      # GPIO ëª¨ë“œ ?‹íŒ…

GPIO.setup(Button, GPIO.IN) # ë²„íŠ¼ ?…ë ¥?¼ë¡œ ?¤ì •

print('Start the GPIO App')
print("Press the button (CTRL-C to exit)")

def getButton(gap=0.3):
    try:
        while True:
            count = 0
            if GPIO.input(Button)==0:
                count=1
                sleep(gap)
                while(GPIO.input(Button)==0):
                    count+=1
                    sleep(gap)
			      #return count
            if(count!=0):
                return count
    except KeyboardInterrupt:      # CTRL-Cë¥??„ë¥´ë©?ë°œìƒ
        GPIO.cleanup()
