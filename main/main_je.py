# -*- coding: utf-8 -*- 
import tts
import obstacleDetect as obsDet
import objectRecognition as objRec
import button
import time
from multiprocessing import Process
import RPi.GPIO as GPIO
import signal
import sys
import os
#import picamera
#from picamera.array import PiRGBArray
import record
import sms
import flag


os.system("sudo rdate -s time.bora.net")
os.system("clear")

server_ip = 'http://210.94.185.47:30010'
imgname='./image.jpg'
#camera = picamera.PiCamera()
#rawCapture = PiRGBArray(camera)


#GPIO Initializing
pin_button1 = 26
pin_button2 = 19
pin_ultra_trg1 = 20
pin_ultra_echo1 = 21
pin_ultra_trg2 = 5
pin_ultra_echo2 = 6
pin_ultra_trg3 =23
pin_ultra_echo3 =24
#pin_ultra_trg4 =
#pin_ultra_echo4 =
pin_vib1 = 12
pin_vib2 = 25

try:
    #os.system("omxplayer /home/pi/Desktop/smartcane/voicefile/start.MP3")
    print("Setting up GPIO...")
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    print("treid gpio cleanup, nothing to clean")
    GPIO.setup(pin_button1,GPIO.IN)
    GPIO.setup(pin_button2,GPIO.IN)
    GPIO.setup(pin_ultra_trg1,GPIO.OUT)
    GPIO.setup(pin_ultra_echo1,GPIO.IN)
    GPIO.setup(pin_ultra_trg2,GPIO.OUT)
    GPIO.setup(pin_ultra_echo2,GPIO.IN)
    GPIO.setup(pin_ultra_trg3,GPIO.OUT)
    GPIO.setup(pin_ultra_echo3,GPIO.IN)
    #GPIO.setup(pin_ultra_trg4,GPIO.OUT)
    #GPIO.setup(pin_ultra_echo4,GPIO.IN)
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
            #flag.setFlag(0)
            #f = open("/home/pi/Desktop/smartcane/blackbox/flag.txt",'w')
            #f.write('0')
            #f.close()
            #time.sleep(2)
            #sms.main()
            
        elif count == 2:
            print(str(pin_button)+" twice")
            #obsDet.main(pin_ultra_trg2,pin_ultra_echo2,pin_vib2)
        elif count >= 3:
            print(str(pin_button)+" long_press")
            #obsDet.main(pin_ultra_trg1,pin_ultra_echo1,pin_vib1)
        time.sleep(0.05)
        
     
def test():
    count=0
    while(True):
        print('test')
        time.sleep(1)
        count+=1
        if count ==10:
            f = open("/home/pi/Desktop/smartcane/blackbox/flag.txt",'w')
            f.write('0')
            f.close()
            time.sleep(2)
            sms.main()
        
            
    
        
try:
    print('Programm Starts')
    pin_list = [[pin_ultra_trg1,pin_ultra_echo1],[pin_ultra_trg2,pin_ultra_echo2],[pin_ultra_trg3,pin_ultra_echo3],[pin_ultra_trg4,pin_ultra_echo4],[pin_vib1,pin_vib2]]
    obsDet.main(pin_list)
    #record.recording(camera)
    #camera.vflip=True
    #objRec.main(camera,rawCapture,imgname,server_ip)
    #t1= Process(target = obsDet.main, args = (pin_ultra_trg1,pin_ultra_echo1,1))
    #t2 = Process(target = obsDet.main, args = (pin_ultra_trg2,pin_ultra_echo2,2))
    #t3 = Process(target = obsDet.main, args = (pin_ultra_trg3,pin_ultra_echo3,3))
    #t3 = Process(target=main,args=(26,))
    #t5 = Process(target=test1,args=())
    #t3 = Process(target = main, args=(pin_button1,))
    #t4 = Process(target = main, args=(pin_button2,))
    #t4 = Process(target = record.recording,args=())
    #print('first '+str(record.flag))
    #t1.start()    
    #t2.start()  
    #t3.start()
    #t4.start()
    #t5.start()
    #t3.join()
    #t4.join()
    #t5.join()
    #t1.join()    
    #t2.join()
    

    #objRec.main(camera,rawCapture,imgname,server_ip)
finally:
    print("finalize")
    GPIO.cleanup()
