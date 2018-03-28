# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import sys
import signal


#GPIO ?€
TRIG = 23 
ECHO = 24 # ?ì½”

MAX_DISTANCE_CM = 300
MAX_DURATION_TIMEOUT = (MAX_DISTANCE_CM * 2 * 29.1) #17460 # 17460us = 300cm

# ?¤ë³´??CTRL + C ?„ë¥´ë©?ì¢…ë£Œ ?˜ê²Œ ì²˜ë¦¬
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        GPIO.cleanup()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# cm ?˜ì‚° ?¨ìˆ˜
# ?„ë‘?´ë…¸ UltraDistSensor ì½”ë“œ?ì„œ ê°€?¸ì˜´
def distanceInCm(duration):
    # ë¬¼ì²´???„ì°©???Œì•„?¤ëŠ” ?œê°„ ê³„ì‚°
    # ?œê°„ = cm / ?Œì† * ?•ë³µ
    # t   = 0.01/340 * 2= 0.000058824ì´?(58.824us)

    # ?¸ì‹ê¹Œì????œê°„
    # t = 0.01/340 = 0.000029412ì´?(29.412us)

    # duration?€ ?•ë³µ ?œê°„?´ë‹ˆ ?¸ì‹ê¹Œì????œê°„?ì„œ 2ë¡??˜ëˆ”
    return (duration/2)/29.1


# ê±°ë¦¬ ?œì‹œ
def print_distance(distance):
    if distance == 0:
        distanceMsg = 'Distance : out of range                   \r'
    else:
        distanceMsg = 'Distance : ' + str(distance) + 'cm' + '        \r'
    sys.stdout.write(distanceMsg)
    sys.stdout.flush()


def main():
    # ?Œì´??GPIO ëª¨ë“œ
    GPIO.setmode(GPIO.BCM)
    VIB=22
    # ?€ ?¤ì •
    GPIO.setup(TRIG, GPIO.OUT) # ?¸ë¦¬ê±?ì¶œë ¥
    GPIO.setup(ECHO, GPIO.IN)  # ?ì½” ?…ë ¥
    GPIO.setup(VIB,GPIO.OUT)
    pwm_vib = GPIO.PWM(VIB, 500)
    pwm_vib.start(100)
    

    print('To Exit, Press the CTRL+C Keys')

    # HC-SR04 ?œì‘ ??? ì‹œ ?€ê¸?    GPIO.output(TRIG, False)
    print('Waiting For Sensor To Ready')
    time.sleep(1) # 1ì´?
    #?œì‘
    print('Start!!')
    while True:
        #171206 ì¤‘ê°„???µì‹  ?ˆë˜??ë¬¸ì œ ê°œì„ ??     
        fail = False
        time.sleep(0.1)
        # ?¸ë¦¬ê±°ë? 10us ?™ì•ˆ High ?ˆë‹¤ê°€ Lowë¡???
        # sleep 0.00001 = 10us
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        timeout = time.time()
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()
            if ((pulse_start - timeout)*1000000) >= MAX_DURATION_TIMEOUT:
                #171206 ì¤‘ê°„???µì‹  ?ˆë˜??ë¬¸ì œ ê°œì„ ??       
                #continue
                fail = True
                break
                
        #171206 ì¤‘ê°„???µì‹  ?ˆë˜??ë¬¸ì œ ê°œì„ ??       
        if fail:
            continue
        timeout = time.time()
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()
            if ((pulse_end - pulse_start)*1000000) >= MAX_DURATION_TIMEOUT:
                print_distance(0) 
                #171206 ì¤‘ê°„???µì‹  ?ˆë˜??ë¬¸ì œ ê°œì„ ??       
                #continue
                fail = True
                break

        #171206 ì¤‘ê°„???µì‹  ?ˆë˜??ë¬¸ì œ ê°œì„ ??       
        if fail:
            continue

        #?¸ì‹ ?œì‘ë¶€??ì¢…ë£Œê¹Œì???ì°¨ê? ë°”ë¡œ ê±°ë¦¬ ?¸ì‹ ?œê°„
        pulse_duration = (pulse_end - pulse_start) * 1000000

        # ?œê°„??cmë¡??˜ì‚°
        distance = distanceInCm(pulse_duration)
        #print(pulse_duration)
        #print('')
        # ?ë¦¬??ë°˜ì˜¬ë¦?        distance = round(distance, 2)
        
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
        #?œì‹œ
        

    GPIO.cleanup()



if __name__ == '__main__':
   main()