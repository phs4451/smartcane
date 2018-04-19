# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import sys
import signal


#GPIO
#24, 25
#TRIG = 20
#ECHO = 21

GPIO.setmode(GPIO.BCM)

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        GPIO.cleanup()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
class obstacleDetect():
    def __init__(self,trig,echo,vib):
        self.TRIG = trig
        self.ECHO = echo
        self.VIB = vib
   
        self.MAX_DISTANCE_CM = 300
        self.MAX_DURATION_TIMEOUT = (self.MAX_DISTANCE_CM*2*29.1)
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)
        GPIO.setup(self.VIB, GPIO.OUT)
        
    def distanceInCm(duration):
        return (duration/2)/29.1
    
    def print_distance(distance):
        if distance == 0:
            distanceMsg = 'Distance : out of range                   \r'
        else:
            distanceMsg = 'Distance : ' + str(distance) + 'cm' + '        \r'
        sys.stdout.write(distanceMsg)
        sys.stdout.flush()
    
    def main(self):
        time.sleep(1)
        pwm_vib = GPIO.PWM(self.VIB, 500)
        pwm_vib.start(100)
        
        print('To Exit, Press the CTRL+C Keys')
        print('Waiting For Sensor To Ready')
        print('Start!!')

        while True:     
            fail = False
            time.sleep(0.1)
            GPIO.output(self.TRIG, True)
            time.sleep(0.00001)
            GPIO.output(self.TRIG, False)
            timeout = time.time()
      
            while GPIO.input(self.ECHO) == 0:
                pulse_start = time.time()
                if ((pulse_start - timeout)*1000000) >= self.MAX_DURATION_TIMEOUT:
                    fail = True
                    break
            if fail:
                continue  
            timeout = time.time()
            while GPIO.input(self.ECHO) == 1:
                pulse_end = time.time()
                if ((pulse_end - pulse_start)*1000000) >= self.MAX_DURATION_TIMEOUT:
                    print_distance(0)
                    fail = True
                    break
       
            if fail:
                continue

            pulse_duration = (pulse_end - pulse_start)*1000000
            distance = self.distanceInCm(pulse_duration)
            
            if distance <= 5 :
                self.print_distance(distance)
                duty = 100
                pwm_vib.ChangeDutyCycle(duty) 
            elif distance <=200:
                self.print_distance(distance)
                duty = 80
                pwm_vib.ChangeDutyCycle(duty)   
            else:
                print("out of range")
                duty = 0
                pwm_vib.ChangeDutyCycle(duty) 
        GPIO.cleanup()
    
if __name__ == '__main__':
   main()
