# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO      # gpio ?¼ì´ë¸ŒëŸ¬ë¦?from time import sleep       # sleep ?¼ì´ë¸ŒëŸ¬ë¦?
from time import sleep

LED = 23
Button = 18
count = 0
conclick = 0

GPIO.setmode(GPIO.BCM)      # GPIO ëª¨ë“œ ?‹íŒ…

GPIO.setup(LED, GPIO.OUT)   # LED ì¶œë ¥?¼ë¡œ ?¤ì •
GPIO.setup(Button, GPIO.IN) # ë²„íŠ¼ ?…ë ¥?¼ë¡œ ?¤ì •

print 'Start the GPIO App'  # ?œì‘???Œë¦¬??
print "Press the button (CTRL-C to exit)"
print "ë²„íŠ¼???ŒëŸ¬ ì£¼ì„¸??"
gap=0.3
try:
        while True:
		count=0
                if GPIO.input(Button)==0:
			count=1
			sleep(gap)
			while(GPIO.input(Button)==0):
				count+=1
				sleep(gap)
		#return count
		if(count!=0):
			print(str(count)+"¹ø ´­·¶½À´Ï´Ù")

except KeyboardInterrupt:      # CTRL-Cë¥??„ë¥´ë©?ë°œìƒ
        GPIO.cleanup()
