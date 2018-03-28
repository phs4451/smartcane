# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import sys
import signal


#GPIO ?�
TRIG = 23 
ECHO = 24 # ?�코

MAX_DISTANCE_CM = 300
MAX_DURATION_TIMEOUT = (MAX_DISTANCE_CM * 2 * 29.1) #17460 # 17460us = 300cm

# ?�보??CTRL + C ?�르�?종료 ?�게 처리
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        GPIO.cleanup()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# cm ?�산 ?�수
# ?�두?�노 UltraDistSensor 코드?�서 가?�옴
def distanceInCm(duration):
    # 물체???�착???�아?�는 ?�간 계산
    # ?�간 = cm / ?�속 * ?�복
    # t   = 0.01/340 * 2= 0.000058824�?(58.824us)

    # ?�식까�????�간
    # t = 0.01/340 = 0.000029412�?(29.412us)

    # duration?� ?�복 ?�간?�니 ?�식까�????�간?�서 2�??�눔
    return (duration/2)/29.1


# 거리 ?�시
def print_distance(distance):
    if distance == 0:
        distanceMsg = 'Distance : out of range                   \r'
    else:
        distanceMsg = 'Distance : ' + str(distance) + 'cm' + '        \r'
    sys.stdout.write(distanceMsg)
    sys.stdout.flush()


def main():
    # ?�이??GPIO 모드
    GPIO.setmode(GPIO.BCM)
    VIB=22
    # ?� ?�정
    GPIO.setup(TRIG, GPIO.OUT) # ?�리�?출력
    GPIO.setup(ECHO, GPIO.IN)  # ?�코 ?�력
    GPIO.setup(VIB,GPIO.OUT)
    pwm_vib = GPIO.PWM(VIB, 500)
    pwm_vib.start(100)
    

    print('To Exit, Press the CTRL+C Keys')

    # HC-SR04 ?�작 ???�시 ?��?    GPIO.output(TRIG, False)
    print('Waiting For Sensor To Ready')
    time.sleep(1) # 1�?
    #?�작
    print('Start!!')
    while True:
        #171206 중간???�신 ?�되??문제 개선??     
        fail = False
        time.sleep(0.1)
        # ?�리거�? 10us ?�안 High ?�다가 Low�???
        # sleep 0.00001 = 10us
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        timeout = time.time()
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()
            if ((pulse_start - timeout)*1000000) >= MAX_DURATION_TIMEOUT:
                #171206 중간???�신 ?�되??문제 개선??       
                #continue
                fail = True
                break
                
        #171206 중간???�신 ?�되??문제 개선??       
        if fail:
            continue
        timeout = time.time()
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()
            if ((pulse_end - pulse_start)*1000000) >= MAX_DURATION_TIMEOUT:
                print_distance(0) 
                #171206 중간???�신 ?�되??문제 개선??       
                #continue
                fail = True
                break

        #171206 중간???�신 ?�되??문제 개선??       
        if fail:
            continue

        #?�식 ?�작부??종료까�???차�? 바로 거리 ?�식 ?�간
        pulse_duration = (pulse_end - pulse_start) * 1000000

        # ?�간??cm�??�산
        distance = distanceInCm(pulse_duration)
        #print(pulse_duration)
        #print('')
        # ?�리??반올�?        distance = round(distance, 2)
        
        if distance <= 5:
          print_distance(distance)
          duty = 100
          pwm_vib.ChangeDutyCycle(duty) 
        elif distance <=15:
          print_distance(distance)
          duty = 80
          pwm_vib.ChangeDutyCycle(duty) 
          
        else:
          print("nononono")
          duty = 0
          pwm_vib.ChangeDutyCycle(duty) 
        #?�시
        

    GPIO.cleanup()



if __name__ == '__main__':
   main()