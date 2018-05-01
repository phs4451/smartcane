# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import sys
import signal

MAX_DISTANCE_CM = 300
MAX_DURATION_TIMEOUT = (MAX_DISTANCE_CM * 2 * 29.1) #17460 # 17460us = 300cm

def distanceInCm(duration):
    return (duration/2)/29.1

def print_distance(distance):
    if distance == 0:
        distanceMsg = 'Distance : out of range                   \r'
    else:
        distanceMsg = 'Distance : ' + str(distance) + 'cm' + '        \r'
    sys.stdout.write(distanceMsg)
    sys.stdout.flush()


def main(pin_ultra_trg,pin_ultra_echo,pin_vib):
    time.sleep(1)
    pwm_vib = GPIO.PWM(pin_vib, 500)
    pwm_vib.start(100)
    
    try:     
        while True:     
            fail = False
            time.sleep(0.1)
            GPIO.output(pin_ultra_trg, True)
            time.sleep(0.00001)
            GPIO.output(pin_ultra_trg, False)

            timeout = time.time()
            
            while GPIO.input(pin_ultra_echo) == 0:
                pulse_start = time.time()
                if ((pulse_start - timeout)*1000000) >= MAX_DURATION_TIMEOUT:
                    fail = True
                    break
                        
            if fail:
                continue
            
            timeout = time.time()
            
            while GPIO.input(pin_ultra_echo) == 1:
                pulse_end = time.time()
                if ((pulse_end - pulse_start)*1000000) >= MAX_DURATION_TIMEOUT:
                    print_distance(0) 
                    fail = True
                    break
        
            if fail:
                continue

            pulse_duration = (pulse_end - pulse_start) * 1000000

            distance = distanceInCm(pulse_duration)
            
            duty = (MAX_DISTANCE_CM-distance)/MAX_DISTANCE_CM *100
            
            if distance <= MAX_DISTANCE_CM :
                print_distance(distance)
                pwm_vib.ChangeDutyCycle(duty)
                duty = 0
            else:
                print("out of range")
                duty = 0
                pwm_vib.ChangeDutyCycle(duty)
            
    except KeyboardInterrupt:
        pwm_vib.stop()
        GPIO.cleanup()
        #sys.exit(0)
if __name__ == '__main__':
   main()
