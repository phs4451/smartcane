# -*- coding: utf-8 -*- 
import time
import RPi.GPIO as GPIO
import signal
import sys
import os

import tts
import obstacleDetect as obsDet
import objectRecognition as objRec
import button
import record
import sms
import flag

import picamera
from picamera.array import PiRGBArray
from multiprocessing import Process, Queue


os.system("clear")

server_ip = 'http://210.94.185.47:30010'
imgname='./image.jpg'
camera = picamera.PiCamera()
rawCapture = PiRGBArray(camera)

##########################GPIO SETUP#################################
#GPIO Initializing
pin_button1 = 26
pin_button2 = 19
pin_ultra_trg1 = 20
pin_ultra_echo1 = 21
pin_ultra_trg2 = 5
pin_ultra_echo2 = 6
pin_ultra_trg3 =23
pin_ultra_echo3 =24
#pin_vib1 = 23
#pin_vib2 = 25

try:
    print("Setting up GPIO...")
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    GPIO.setup(pin_button1,GPIO.IN)
    GPIO.setup(pin_button2,GPIO.IN)
    GPIO.setup(pin_ultra_trg1,GPIO.OUT)
    GPIO.setup(pin_ultra_echo1,GPIO.IN)
    GPIO.setup(pin_ultra_trg2,GPIO.OUT)
    GPIO.setup(pin_ultra_echo2,GPIO.IN)
    GPIO.setup(pin_ultra_trg3,GPIO.OUT)
    GPIO.setup(pin_ultra_echo3,GPIO.IN)
    #GPIO.setup(pin_vib1,GPIO.OUT)
    #GPIO.setup(pin_vib2,GPIO.OUT)
    print("GPIO SETUP Complete")
except:
    print("GPIO SETUP ERROR")
##########################GPIO SETUP END#################################

flag.initFlag()

def main(pin_button,q):
    while(True):
        print('button')
        count= button.main(pin_button)
        if count == 1: #yolo
            p = Process(objRec(camera,rawCapture,imgname,server_ip)
            q.put(p)
            if flag.getFlag() == 1
            p.start
        elif count == 2: #crosswalk 
            print(str(pin_button)+" twice")
            #obsDet.main(pin_ultra_trg2,pin_ultra_echo2,pin_vib2)
        elif count >= 3: #sos
            print(str(pin_button)+" long_press")
            #obsDet.main(pin_ultra_trg1,pin_ultra_echo1,pin_vib1)
        time.sleep(0.05)

def cancel(pin_button): #cancel button's pin num is 26.
    while(True):
	printt('cancel listening...')
	count = button.main(pin_button)
	if count == 1:
		#kill process
            target = q.get()
            target.terminate()
	elif count>=2:
		#change phone num in sos.

try:
    global t4
    print('Programm Starts')
    #pin_list = [[pin_ultra_trg1,pin_ultra_echo1],[pin_ultra_trg2,pin_ultra_echo2],[pin_ultra_trg3,pin_ultra_echo3]]
    #obsDet.main(pin_list)
    #record.recording(camera)
    #camera.vflip=True
    #objRec.main(camera,rawCapture,imgname,server_ip)
    #t1= Process(target = obsDet.main, args = (pin_ultra_trg1,pin_ultra_echo1,1))
    #t2 = Process(target = obsDet.main, args = (pin_ultra_trg2,pin_ultra_echo2,2))
    #t3 = Process(target = obsDet.main, args = (pin_ultra_trg3,pin_ultra_echo3,3))
    #t3 = Process(target=test,args=())
    #t5 = Process(target=test1,args=())
    t3 = Process(target = main, args=(pin_button1,))
    t4 = Process(target = record.recording,args=())
    #print('first '+str(record.flag))
    #t1.start()    
    #t2.start()  
    t3.start()
    t4.start()
    #t5.start()
    t3.join()
    t4.join()
    #t5.join()
    #t1.join()    
    #t2.join()
    #objRec.main(camera,rawCapture,imgname,server_ip)
finally:
    print("finalize")
    GPIO.cleanup()



