
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import sys
import signal
import numpy as np
import vibrate_je

MAX_DISTANCE_CM = 300
MAX_DURATION_TIMEOUT = (MAX_DISTANCE_CM * 2 * 29.1) #17460 # 17460us = 300cm

dist_check=[]

def distanceInCm(duration):
    return (duration/2)/29.1

def main(pin_list):

    while True:
        #s1 = getDistance(pin_list[0][0],pin_list[0][1],pin_list[3][0],pin_list[3][1],1)
        #s2 = getDistance(pin_list[1][0],pin_list[1][1],pin_list[3][0],pin_list[3][1],2)
        #s3 = getDistance(pin_list[2][0],pin_list[2][1],pin_list[3][0],pin_list[3][1],3)
        #print("Sensor1: "+str(s1)+"\tSensor2: "+str(s2)+"\tSensor3: "+str(s3))
        s1 = getDistance(pin_list[0][0],pin_list[0][1],pin_list[4][0],pin_list[4][1],pin_list[4][2],1)
        s2 = getDistance(pin_list[1][0],pin_list[1][1],pin_list[4][0],pin_list[4][1],pin_list[4][2],2)
        s3 = getDistance(pin_list[2][0],pin_list[2][1],pin_list[4][0],pin_list[4][1],pin_list[4][2],3)
        s4 = getDistance(pin_list[3][0],pin_list[3][1],pin_list[4][0],pin_list[4][1],pin_list[4][2],4)
        print("Sensor1: "+str(s1)+"\tSensor2: "+str(s2)+"\tSensor3: "+str(s3)+"\tSensor4: "+str(s4))


def moving_average(a,n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:]-ret[:-n]    
    return ret[n-1]/n
    
def distCheck(pin_vib3):
    if len(dist_check) <3:
        g = np.gradient(moving_average(dist_check))
    else:
        return
    if min(g, default =0) <=10:
        vibrate_je.vibrate1(pin_vib3)
               
def clear_dist():     #일정 길이 이상으로 저장되기 전 리스트 앞부분 삭제
    if len(dist_check)>=30:
        dist_check[:15] = []
                   
def getDistance(pin_ultra_trg,pin_ultra_echo,pin_vib1, pin_vib2, pin_vib3, index):
    time.sleep(0.01)
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
                fail = True
                break

        pulse_duration = (pulse_end - pulse_start) * 1000000

        distance = int(distanceInCm(pulse_duration))
        
        
        if 0< distance <= MAX_DISTANCE_CM :
            if index ==4:
                clear_dist()
                dist_check.append(distance)
                distCheck(pin_vib3)
                
            elif index!=4 and distance <= 180:
                vibrate_je.vibrate2(index,pin_vib1, pin_vib2)
            return distance
        else:
            return MAX_DISTANCE_CM

    except KeyboardInterrupt:
        GPIO.cleanup()
        
if __name__ == '__main__':
   main()

