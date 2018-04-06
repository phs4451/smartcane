from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class Button():
	def __init__(self,pin):
		self.pin = pin
		GPIO.setup(pin, GPIO.IN)

	def getButton(gap=0.3):
		try:
			while True:
				count = 0
				if GPIO.input(Button)==0:
					count=1
					sleep(gap)
					while(GPIO.input(Button)==0):
						count+=1
						sleep(gap)
					#return count
				if(count!=0):
					return count
		except KeyboardInterrupt:      # CTRL-C???꾨Ⅴ�?諛쒖�?
			GPIO.cleanup()
	def getPin():
		return self.pin
