# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import sys
import signal
import numpy as np

MAX_DISTANCE_CM = 300
MAX_DURATION_TIMEOUT = (MAX_DISTANCE_CM * 2 * 29.1) #17460 # 17460us = 300cm
dist_check=[[],[],[]]

def distanceInCm(duration):
    return (duration/2)/29.1

def main(pin_list):
    while True:
        s1 = getDistance(pin_list[0][0],pin_list[0][1],1)
        s2 = getDistance(pin_list[1][0],pin_list[1][1],2)
        s3 = getDistance(pin_list[2][0],pin_list[2][1],3)
        print("Sensor1: "+str(s1)+"\tSensor2: "+str(s2)+"\tSensor3: "+str(s3))
        #distCheck()


def moving_average(a,n=6):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:]-ret[:-n]
    
    return ret[n-1]/n
    
def distCheck():
    warning = []
    for dist_list in dist_check:
        g = np.gradient(moving_average(dist_list))   #gradient of moving average list
        
        if max(np.diff(g)) >100:  #기울기 값의 차이
           warning.append(dist_check.index(dist_list) + 1)  #인덱스 반환
    return warning
                

def clear_dist():     #일정 길이 이상으로 저장되기 전 리스트 앞부분 삭제
    for dist_list in dist_check:
        if len(dist_list)>=100:
           dist_list[:20] = []
                   
def getDistance(pin_ultra_trg,pin_ultra_echo,index):
    time.sleep(0.1)
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
        
        if distance <= MAX_DISTANCE_CM :
            #clear_dist()
            #dist_check[index-1].append(distance)
            # warning = distCheck()
            return distance
        else:
            return 0

    except KeyboardInterrupt:
        GPIO.cleanup()
if __name__ == '__main__':
   main()
