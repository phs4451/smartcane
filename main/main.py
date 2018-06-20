# -*- coding: utf-8 -*- 
import tts
import obstacleDetect as obsDet
import objectRecognition as objRec
import button
import record
import flag
import blockdetect
import sound
import stt
import signal
import sys
import os
import time
import RPi.GPIO as GPIO
from multiprocessing import Process

#os.system("sudo rdate -s time.bora.net")
GPIO.cleanup()
os.system("clear")

#GPIO Initializing
pin_button1 = 13
pin_button2 = 19
#pin_SW = 18
pin_ultra_trg1 = 20
pin_ultra_echo1 = 21
pin_ultra_trg2 = 5
pin_ultra_echo2 = 6
pin_ultra_trg3 =23

pin_ultra_echo3 =24
pin_ultra_trg4 = 17
pin_ultra_echo4 = 27
pin_vib1 = 16
pin_vib2 = 25
pin_vib3 = 12

try:
    sound.start()
    flag.initFlag(flag.camera)
    flag.initFlag(flag.vibrate)
    
    print("Setting up GPIO...")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_button1,GPIO.IN)
    GPIO.setup(pin_button2,GPIO.IN)
    #GPIO.setup(pin_SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(pin_ultra_trg1,GPIO.OUT)
    GPIO.setup(pin_ultra_echo1,GPIO.IN)
    GPIO.setup(pin_ultra_trg2,GPIO.OUT)
    GPIO.setup(pin_ultra_echo2,GPIO.IN)
    GPIO.setup(pin_ultra_trg3,GPIO.OUT)
    GPIO.setup(pin_ultra_echo3,GPIO.IN)
    GPIO.setup(pin_ultra_trg4,GPIO.OUT)
    GPIO.setup(pin_ultra_echo4,GPIO.IN)
    GPIO.setup(pin_vib1,GPIO.OUT)
    GPIO.setup(pin_vib2,GPIO.OUT)
    GPIO.setup(pin_vib3,GPIO.OUT)
    print("GPIO SETUP Complete")
except:
    print("GPIO SETUP ERROR")

def button1(pin_button):
    
    while(True):
        print('button')
        count= button.main(pin_button)
        
        if count == 1:
            print(str(pin_button)+" once")
            flag.setFlag(0,flag.camera)
            time.sleep(0.15)
            objRec.main()
            flag.setFlag(1,flag.camera)
            
        elif count == 2:
            print(str(pin_button)+" twice")
            flag.setFlag(0,flag.camera)
            time.sleep(0.15)
            blockdetect.main()
            flag.setFlag(1,flag.camera)
            
        elif count >= 3:
            import sms
            print(str(pin_button)+" long_press")
            flag.setFlag(0,flag.camera)
            time.sleep(0.15)
            sms.main()
            flag.setFlag(1,flag.camera)
            
        time.sleep(0.05)
        
def button2(pin_button):
    
    while(True):
        print('button')
        count= button.main(pin_button)
        
        if count == 1:
            vib_flag = flag.getFlag(flag.vibrate)
            if vib_flag == '1':
                os.system('mplayer voicefile/vibrateoff.mp3')
                print("vibrate off")
                flag.setFlag(0,flag.vibrate)
            elif vib_flag == '0':
                os.system('mplayer voicefile/vibrateon.mp3')
                print("vibrate on")
                flag.setFlag(1,flag.vibrate)
                
        elif count >= 3:
            stt.main()

        time.sleep(0.05)
                
try:
    print('Programm Starts')
    #pin_list = [[pin_ultra_trg1,pin_ultra_echo1],[pin_ultra_trg2,pin_ultra_echo2],[pin_ultra_trg3,pin_ultra_echo3],[pin_vib1,pin_vib2],pin_SW]
    #obsDet.main(pin_list)
    #pin_list = [[pin_ultra_trg1,pin_ultra_echo1],[pin_ultra_trg2,pin_ultra_echo2],[pin_ultra_trg3,pin_ultra_echo3],[pin_ultra_trg4,pin_ultra_echo4],[pin_vib1,pin_vib2,pin_vib3],pin_SW]
    pin_list = [[pin_ultra_trg1,pin_ultra_echo1],[pin_ultra_trg2,pin_ultra_echo2],[pin_ultra_trg3,pin_ultra_echo3],[pin_ultra_trg4,pin_ultra_echo4],[pin_vib1,pin_vib2,pin_vib3]]
    
    t1= Process(target = obsDet.main, args=(pin_list,))
    t2 = Process(target = button1,args=(pin_button1,))
    t3 = Process(target = record.recording,args=())
    t1.start()
    t2.start()
    t3.start()
    button2(pin_button2)
    
    t1.join()
    t2.join()
    t3.join()
    
finally:
    sound.finish()
    print("main stop -------------------------- Cleaning up GPIO...")
    GPIO.cleanup()



