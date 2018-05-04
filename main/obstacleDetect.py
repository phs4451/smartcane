# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import sys
import signal

MAX_DISTANCE_CM = 300
MAX_DURATION_TIMEOUT = (MAX_DISTANCE_CM * 2 * 29.1) #17460 # 17460us = 300cm

def distanceInCm(duration):
    return (duration/2)/29.1

def print_distance(distance,index):
    distance = round(distance,2)
    if distance == 0:
        distanceMsg = str(index)+' Distance : out of range                   \r'
    else:
        distanceMsg = str(index)+'Distance : ' + str(distance) + 'cm' + '        \r'
    print(distanceMsg)

#def getDistance(trig,echo,index):
    #GPIO.output(trig,False)
    #time.sleep(0.1)
    #GPIO.output(trig,True)
    #time.sleep(0.00001)
    #GPIO.output(trig,False)
    
    #while GPIO.input(echo) ==0 :
        #pulse_start = time.time()
        #if ((pulse_start - timeout)*1000000) >= MAX_DURATION_TIMEOUT:
            #fail = True
            #break

def main(pin_list):
    while True:
        s1 = getDistance(pin_list[0][0],pin_list[0][1],1)
        s2 = getDistance(pin_list[1][0],pin_list[1][1],2)
        s3 = getDistance(pin_list[2][0],pin_list[2][1],3)
        print("Sensor1: "+str(s1)+"\tSensor2: "+str(s2)+"\tSensor3: "+str(s3))


def getDistance(pin_ultra_trg,pin_ultra_echo,index):
    time.sleep(1)
    pulse_start = 0
    pulse_end = 0
    distance = 0
    pulse_duration = 0
    try:
        fail = False
        time.sleep(0.01)
        GPIO.output(pin_ultra_trg, True)
        time.sleep(0.00001)
        GPIO.output(pin_ultra_trg, False)

        timeout = time.time()
        
        while GPIO.input(pin_ultra_echo) == 0:
            pulse_start = time.time()
            if ((pulse_start - timeout)*1000000) >= MAX_DURATION_TIMEOUT:
                fail = True
                break
        
        timeout = time.time()
        
        while GPIO.input(pin_ultra_echo) == 1:
            pulse_end = time.time()
            if ((pulse_end - pulse_start)*1000000) >= MAX_DURATION_TIMEOUT:
                #print_distance(0) 
                fail = True
                break

        pulse_duration = (pulse_end - pulse_start) * 1000000

        distance = distanceInCm(pulse_duration)
        distance = round(distance,2)
        duty = (MAX_DISTANCE_CM-distance)/MAX_DISTANCE_CM *100
        
        if distance <= MAX_DISTANCE_CM :
            #print_distance(distance)
            return distance
            #pwm_vib.ChangeDutyCycle(duty)
            duty = 0
        else:
            print("out of range")
            return 0
            duty = 0
            #pwm_vib.ChangeDutyCycle(duty)

    except KeyboardInterrupt:
        #pwm_vib.stop()
        GPIO.cleanup()
        #sys.exit(0)
if __name__ == '__main__':
   main()
