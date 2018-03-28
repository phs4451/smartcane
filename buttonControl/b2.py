# -*- coding: utf-8 -*-
import picamera
from picamera.array import PiRGBArray
import time
import requests
import base64
import json
from collections import OrderedDict
import pprint
from PIL import Image

import RPi.GPIO as GPIO      # gpio ?�이브러�?from time import sleep       # sleep ?�이브러�?
from time import sleep

LED = 23
Button = 18
count = 0


GPIO.setmode(GPIO.BCM)      # GPIO 모드 ?�팅

GPIO.setup(LED, GPIO.OUT)   # LED 출력?�로 ?�정
GPIO.setup(Button, GPIO.IN) # 버튼 ?�력?�로 ?�정
camera = picamera.PiCamera()
capture = PiRGBArray(camera)
print 'Start the GPIO App'  # ?�작???�리??
print "Press the button (CTRL-C to exit)"
try:
        while True:
		flag = False
                if GPIO.input(Button)==0:
			count+=1
			sleep(0.01)
			while(GPIO.input(Button)):
	                        count+=1
				sleep(0.01)
			
			'''
                        if count == 3:
                           GPIO.output(LED, True)
                           print "Button was Pressed!"  
                           imgname='./image9.jpg'
                           camera.capture(capture,format='rgb',use_video_port=True)
                           capture = Image.fromarray(capture.array)
                           capture.save(imgname)
                           count=0
                        else:
                           print "Button was Pressed!"
			'''
                                     
                                                                     
                else:
			print(count)
			count = 0
			
			'''
                        GPIO.output(LED, False)
                        print "Button was Not Pressed!"
                        print 'count = ',count
			'''
                        
                        
except KeyboardInterrupt:      # CTRL-C�??�르�?발생
        GPIO.cleanup()
