# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import sys
import signal


#GPIO
#24, 25
TRIG = 20
ECHO = 21

MAX_DISTANCE_CM = 300
MAX_DURATION_TIMEOUT = (MAX_DISTANCE_CM * 2 * 29.1) #17460 # 17460us = 300cm

GPIO.setmode(GPIO.BCM)
VIB=12
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(VIB,GPIO.OUT)

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        GPIO.cleanup()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def distanceInCm(duration):
    return (duration/2)/29.1

def print_distance(distance):
    if distance == 0:
        distanceMsg = 'Distance : out of range                   \r'
    else:
        distanceMsg = 'Distance : ' + str(distance) + 'cm' + '        \r'
    sys.stdout.write(distanceMsg)
    sys.stdout.flush()


def main():
    time.sleep(1)
    pwm_vib = GPIO.PWM(VIB, 500)
    pwm_vib.start(100)
    

    print('To Exit, Press the CTRL+C Keys')
    print('Waiting For Sensor To Ready')
    print('Start!!')
    while True:     
        fail = False
        time.sleep(0.1)
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        timeout = time.time()
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()
            if ((pulse_start - timeout)*1000000) >= MAX_DURATION_TIMEOUT:
                fail = True
                break
                       
        if fail:
            continue
        timeout = time.time()
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()
            if ((pulse_end - pulse_start)*1000000) >= MAX_DURATION_TIMEOUT:
                print_distance(0) 
                fail = True
                break
       
        if fail:
            continue

        pulse_duration = (pulse_end - pulse_start) * 1000000


        distance = distanceInCm(pulse_duration)
        
        if distance <= 5 :
          print_distance(distance)
          duty = 100
          pwm_vib.ChangeDutyCycle(duty) 
        elif distance <=200:
          print_distance(distance)
          duty = 80
          pwm_vib.ChangeDutyCycle(duty) 
          
        else:
          print("out of range")
          duty = 0
          pwm_vib.ChangeDutyCycle(duty) 

        

    GPIO.cleanup()



if __name__ == '__main__':
   main()
