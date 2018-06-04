# -*- coding: utf-8 -*- 
import tts
import obstacleDetect as obsDet
import objectRecognition as objRec
import button
import record
import sms
import flag
import blockdetect
import sound

import signal
import sys
import os
import time
import RPi.GPIO as GPIO
from multiprocessing import Process

os.system("sudo rdate -s time.bora.net")
os.system("clear")

#GPIO Initializing
pin_button1 = 26
pin_button2 = 19
pin_ultra_trg1 = 20
pin_ultra_echo1 = 21
pin_ultra_trg2 = 5
pin_ultra_echo2 = 6
pin_ultra_trg3 =23
pin_ultra_echo3 =24
pin_vib1 = 12
pin_vib2 = 25

try:
    sound.start()
    flag.initFlag()
    print("Setting up GPIO...")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_button1,GPIO.IN)
    GPIO.setup(pin_button2,GPIO.IN)
    GPIO.setup(pin_ultra_trg1,GPIO.OUT)
    GPIO.setup(pin_ultra_echo1,GPIO.IN)
    GPIO.setup(pin_ultra_trg2,GPIO.OUT)
    GPIO.setup(pin_ultra_echo2,GPIO.IN)
    GPIO.setup(pin_ultra_trg3,GPIO.OUT)
    GPIO.setup(pin_ultra_echo3,GPIO.IN)
    GPIO.setup(pin_vib1,GPIO.OUT)
    GPIO.setup(pin_vib2,GPIO.OUT)
    print("GPIO SETUP Complete")
except:
    print("GPIO SETUP ERROR")

def main(pin_button):
    while(True):
        print('button')
        count= button.main(pin_button)
        
        if count == 1:
            print(str(pin_button)+" once")
            sound.camera()
            flag.setFlag(0)
            time.sleep(0.15)
            objRec.main()
            flag.setFlag(1)
            
        elif count == 2:
            print(str(pin_button)+" twice")
            flag.setFlag(0)
            time.sleep(0.15)
            sound.camera()
            blockdetect.main()
            flag.setFlag(1)
            
        elif count >= 3:
            print(str(pin_button)+" long_press")
            flag.setFlag(0)
            time.sleep(0.15)
            #sound.mms()
            sms.main()
            flag.setFlag(1)
            #obsDet.main(pin_ultra_trg1,pin_ultra_echo1,pin_vib1)
        time.sleep(0.05)  
        
try:
    print('Programm Starts')
    
    pin_list = [[pin_ultra_trg1,pin_ultra_echo1],[pin_ultra_trg2,pin_ultra_echo2],[pin_ultra_trg3,pin_ultra_echo3],[pin_vib1,pin_vib2]]
    #obsDet.main(pin_list)
    t1= Process(target = obsDet.main, args=(pin_list,))
    t2 = Process(target = main,args=(pin_button1,))
    t3 = Process(target = record.recording,args=())
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    
finally:
    sound.finish()
    print("Cleaning up GPIO...")
    GPIO.cleanup()



