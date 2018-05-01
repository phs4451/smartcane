# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from time import sleep

def main(pin_button,gap=0.3):
    try:
        count = 0
        while True:
            if GPIO.input(pin_button)==0:
                count=1
                sleep(gap)
                while(GPIO.input(pin_button)==0):
                    count+=1
                    sleep(gap)
            if(count!=0):
                return count
    except KeyboardInterrupt:      # CTRL-CÎ•??ÑÎ•¥Î©?Î∞úÏÉù
        GPIO.cleanup()
