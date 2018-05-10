import time
import picamera
import RPi.GPIO as GPIO
import os

starttime = str(int(time.time()))
with picamera.PiCamera() as camera:
       camera.start_preview()
       camera.start_recording('/home/pi/Desktop/smartcane/blackbox/'+starttime+'.h264')   
       time.sleep(5)
       camera.stop_preview()
       camera.stop_recording()
       os.system('MP4Box -add /home/pi/Desktop/smartcane/blackbox/'+starttime+'.h264 /home/pi/Desktop/smartcane/blackbox/'+starttime+'.mp4') 
       os.system('rm '+starttime+'.h264')
