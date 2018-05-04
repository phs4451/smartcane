import tts
import obstacleDetect as obsDet
import button
import time
from multiprocessing import Process
import RPi.GPIO as GPIO
import signal
import sys
import os

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
#pin_vib1 = 23
#pin_vib2 = 25

try:
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

def main(pin_button):
    while(True):
        count= button.main(pin_button)
        if count == 1:
            print(str(pin_button)+" once")
        elif count == 2:
            print(str(pin_button)+" twice")
            #obsDet.main(pin_ultra_trg2,pin_ultra_echo2,pin_vib2)
        elif count >= 3:
            print(str(pin_button)+" long_press")
            #obsDet.main(pin_ultra_trg1,pin_ultra_echo1,pin_vib1)
        time.sleep(0.05)
        
try:
    pin_list = [[pin_ultra_trg1,pin_ultra_echo1],[pin_ultra_trg2,pin_ultra_echo2],[pin_ultra_trg3,pin_ultra_echo3]]
    obsDet.main(pin_list)
    #t1= Process(target = obsDet.main, args = (pin_ultra_trg1,pin_ultra_echo1,1))
    #t2 = Process(target = obsDet.main, args = (pin_ultra_trg2,pin_ultra_echo2,2))
    #t3 = Process(target = obsDet.main, args = (pin_ultra_trg3,pin_ultra_echo3,3))
    #t1.start()
    #t2.start()
    #t3.start()
    #t1.join()
    #t2.join()
    #t3.join()
finally:
    print("finalize")
    GPIO.cleanup()



