# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import sys
import signal


#GPIO ?
TRIG = 23 
ECHO = 24 # ?μ½

MAX_DISTANCE_CM = 300
MAX_DURATION_TIMEOUT = (MAX_DISTANCE_CM * 2 * 29.1) #17460 # 17460us = 300cm

# ?€λ³΄??CTRL + C ?λ₯΄λ©?μ’λ£ ?κ² μ²λ¦¬
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        GPIO.cleanup()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# cm ?μ° ?¨μ
# ?λ?΄λΈ UltraDistSensor μ½λ?μ κ°?Έμ΄
def distanceInCm(duration):
    # λ¬Όμ²΄???μ°©???μ?€λ ?κ° κ³μ°
    # ?κ° = cm / ?μ * ?λ³΅
    # t   = 0.01/340 * 2= 0.000058824μ΄?(58.824us)

    # ?ΈμκΉμ????κ°
    # t = 0.01/340 = 0.000029412μ΄?(29.412us)

    # duration? ?λ³΅ ?κ°?΄λ ?ΈμκΉμ????κ°?μ 2λ‘??λ
    return (duration/2)/29.1


# κ±°λ¦¬ ?μ
def print_distance(distance):
    if distance == 0:
        distanceMsg = 'Distance : out of range                   \r'
    else:
        distanceMsg = 'Distance : ' + str(distance) + 'cm' + '        \r'
    sys.stdout.write(distanceMsg)
    sys.stdout.flush()


def main():
    # ?μ΄??GPIO λͺ¨λ
    GPIO.setmode(GPIO.BCM)
    VIB=22
    # ? ?€μ 
    GPIO.setup(TRIG, GPIO.OUT) # ?Έλ¦¬κ±?μΆλ ₯
    GPIO.setup(ECHO, GPIO.IN)  # ?μ½ ?λ ₯
    GPIO.setup(VIB,GPIO.OUT)
    pwm_vib = GPIO.PWM(VIB, 500)
    pwm_vib.start(100)
    

    print('To Exit, Press the CTRL+C Keys')

    # HC-SR04 ?μ ??? μ ?κΈ?    GPIO.output(TRIG, False)
    print('Waiting For Sensor To Ready')
    time.sleep(1) # 1μ΄?
    #?μ
    print('Start!!')
    while True:
        #171206 μ€κ°???΅μ  ?λ??λ¬Έμ  κ°μ ??     
        fail = False
        time.sleep(0.1)
        # ?Έλ¦¬κ±°λ? 10us ?μ High ?λ€κ° Lowλ‘???
        # sleep 0.00001 = 10us
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        timeout = time.time()
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()
            if ((pulse_start - timeout)*1000000) >= MAX_DURATION_TIMEOUT:
                #171206 μ€κ°???΅μ  ?λ??λ¬Έμ  κ°μ ??       
                #continue
                fail = True
                break
                
        #171206 μ€κ°???΅μ  ?λ??λ¬Έμ  κ°μ ??       
        if fail:
            continue
        timeout = time.time()
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()
            if ((pulse_end - pulse_start)*1000000) >= MAX_DURATION_TIMEOUT:
                print_distance(0) 
                #171206 μ€κ°???΅μ  ?λ??λ¬Έμ  κ°μ ??       
                #continue
                fail = True
                break

        #171206 μ€κ°???΅μ  ?λ??λ¬Έμ  κ°μ ??       
        if fail:
            continue

        #?Έμ ?μλΆ??μ’λ£κΉμ???μ°¨κ? λ°λ‘ κ±°λ¦¬ ?Έμ ?κ°
        pulse_duration = (pulse_end - pulse_start) * 1000000

        # ?κ°??cmλ‘??μ°
        distance = distanceInCm(pulse_duration)
        #print(pulse_duration)
        #print('')
        # ?λ¦¬??λ°μ¬λ¦?        distance = round(distance, 2)
        
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
        #?μ
        

    GPIO.cleanup()



if __name__ == '__main__':
   main()