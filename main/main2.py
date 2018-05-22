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
from multiprocessing import Process, Queue,Pool

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

def main(q):
    count = 0
    while(True):
        pid = os.getpid()
        print('button '+str(pid))
        #count= button.main(pin_button)
        count += 1
        
        if count == 50: #yolo
            #p = Process(objRec(camera,rawCapture,imgname,server_ip)
            newpid = os.fork()
            #if flag.getFlag() == 1
            if newpid ==0:
                sayHi()
            else:
                
                
            q.put()
            p2 = Process(target=cancel(),args=(q,))
            p.start()
            p2.start()
            p.join()
            p2.join()
        '''
        elif count == 2: #crosswalk 
            print(str(pin_button)+" twice")
            #obsDet.main(pin_ultra_trg2,pin_ultra_echo2,pin_vib2)
        elif count >= 3: #sos
            print(str(pin_button)+" long_press")
            #obsDet.main(pin_ultra_trg1,pin_ultra_echo1,pin_vib1)
        '''
        time.sleep(0.1)

def cancel(q): #pin_button): #cancel button's pin num is 26.
    count = 0
    while(True):
        pid = os.getpid()
        print('cancel listening...'+str(pid))
        #count = button.main(pin_button)
        if count == 100:
            #kill process
            print("try")
            target = q.get()
            print(type(target))
            target.terminate()
            count = 0
        #elif count>=2:
            #change phone num in sos.
        count += 1
        time.sleep(0.1)

def sayHi():
    while True:
        pid = os.getpid()
        time.sleep(1)
        print("Hi~ "+str(pid))

try:
    print('Programm Starts')
    q = Queue()
    
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
    t3= Process(target = main,args = (q,))
    #t3 = Process(target = main, args=(pin_button1,))
    #t4 = Process(target = cancel,args=(q,))
    #t4 = Process(target = record.recording,args=())
    #print('first '+str(record.flag))
    #t1.start()    
    #t2.start()  
    t3.start()
    #t4.start()
    #t5.start()
    t3.join()
    #t4.join()
    #t5.join()
    #t1.join()    
    #t2.join()
    #objRec.main(camera,rawCapture,imgname,server_ip)
finally:
    print("finalize")
    GPIO.cleanup()



