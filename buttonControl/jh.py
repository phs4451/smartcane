# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO      # gpio ?�이브러�?from time import sleep       # sleep ?�이브러�?
from time import sleep

LED = 23
Button = 18
count = 0
conclick = 0

GPIO.setmode(GPIO.BCM)      # GPIO 모드 ?�팅

GPIO.setup(LED, GPIO.OUT)   # LED 출력?�로 ?�정
GPIO.setup(Button, GPIO.IN) # 버튼 ?�력?�로 ?�정

print 'Start the GPIO App'  # ?�작???�리??
print "Press the button (CTRL-C to exit)"
print "버튼???�러 주세??"
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
			print(str(count)+"�� �������ϴ�")

except KeyboardInterrupt:      # CTRL-C�??�르�?발생
        GPIO.cleanup()
