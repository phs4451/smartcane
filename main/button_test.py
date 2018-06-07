import RPi.GPIO as gpio
sw = 18
gpio.setmode(gpio.BCM)
gpio.setup(sw,gpio.IN,pull_up_down=gpio.PUD_UP)

import time


while True:
    key_in = gpio.input(sw)
    print(key_in)
    time.sleep(0.5)
