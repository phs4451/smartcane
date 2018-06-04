
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import sys
import signal
import numpy as np
import vibrate_je

MAX_DISTANCE_CM = 300
MAX_DURATION_TIMEOUT = (MAX_DISTANCE_CM * 2 * 29.1) #17460 # 17460us = 300cm
dist_check=[[],[],[]]
avg_list=[[],[],[]]
detect_threshold = 80

def distanceInCm(duration):
    return (duration/2)/29.1

def main(pin_list):
    while True:
        time.sleep(0.3)
        s1 = getDistance(pin_list[0][0],pin_list[0][1],pin_list[3][0],pin_list[3][1],1)
        s2 = getDistance(pin_list[1][0],pin_list[1][1],pin_list[3][0],pin_list[3][1],2)
        s3 = getDistance(pin_list[2][0],pin_list[2][1],pin_list[3][0],pin_list[3][1],3)
        print("Sensor1: "+str(s1)+"\tSensor2: "+str(s2)+"\tSensor3: "+str(s3))
        
        for i,dist in enumerate(dist_check):
            if len(dist)>=10:
                temp  = []
                temp = moving_average(dist)
                if temp[-1] <= detect_threshold:
                    print(i+1,temp[-1],len(dist))
                    vibrate_je.vibrate2(i+1,temp[-1],pin_list[3][0],pin_list[3][1])
                    break;
            #avg.append(moving_average(dist_check[i]))
            #if avg[i][-1] - avg[i][-4]>10 and len(avg[i]) > 5:
                #vibrate_je(i+1,avg[i][-1],pin_vib1,pin_vib2)
        
        #s1 = getDistance(pin_list[0][0],pin_list[0][1],pin_list[4][0],pin_list[4][1],1)
        #s2 = getDistance(pin_list[1][0],pin_list[1][1],pin_list[4][0],pin_list[4][1],2)
        #s3 = getDistance(pin_list[2][0],pin_list[2][1],pin_list[4][0],pin_list[4][1],3)
        #s4 = getDistance(pin_list[3][0],pin_list[3][1],pin_list[4][0],pin_list[4][1],3)
        #print("Sensor1: "+str(s1)+"\tSensor2: "+str(s2)+"\tSensor3: "+str(s3)+"\tSensor4: "+str(s4))
        #distCheck(pin_list[4][0],pin_list[4][1])

def moving_average(a,n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:]-ret[:-n]
    return ret[n-1:]//n
    #return ret[-n:]/n
    
def distCheck(pin_vib1, pin_vib2):
    warning = []
    for dist_list in dist_check:
        #print("Distance List : ",dist_list)
        if len(dist_list)>3:
            g = np.gradient(moving_average(dist_list))
        else:
            #g = np.gradient(moving_average(dist_list,1))   #gradient of moving average list
            return

        if min(g,default = 0 ) <= -10:  
            warning.append(dist_check.index(dist_list) + 1)  #인덱스 반환
    
    #vibrate_je.main(warning,pin_vib1, pin_vib2)
    
    return warning
                

def clear_dist():     #일정 길이 이상으로 저장되기 전 리스트 앞부분 삭제
    for dist_list in dist_check:
        if len(dist_list)>=30:
            dist_list[:15] = []
                   
def getDistance(pin_ultra_trg,pin_ultra_echo,pin_vib1, pin_vib2, index):
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
                #print_distance(0) 
                fail = True
                break

        pulse_duration = (pulse_end - pulse_start) * 1000000

        distance = int(distanceInCm(pulse_duration))
        
        
        if 0< distance <= MAX_DISTANCE_CM :
            clear_dist()
            dist_check[index-1].append(distance)
            #print(dist_check[0],dist_check[1],dist_check[2])
            #warning = distCheck()
            #print(warning)
            #if distance <= detect_threshold:
                #vibrate_je.vibrate2(index,distance, pin_vib1, pin_vib2)
            return distance
        else:
            clear_dist()
            dist_check[index-1].append(MAX_DISTANCE_CM)
            #print(dist_check[0],dist_check[1],dist_check[2])
            return MAX_DISTANCE_CM

    except KeyboardInterrupt:
        GPIO.cleanup()
        print('obstacle stop')
if __name__ == '__main__':
   main()
