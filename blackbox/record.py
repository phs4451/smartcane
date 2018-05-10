import time
import picamera
import RPi.GPIO as GPIO
import os



starttime = str(int(time.time()))
with picamera.PiCamera() as camera:
          camera.start_preview()
          camera.start_recording('/home/pi/Desktop/smartcane/blackbox/'+starttime+'.h264')   
    
    
          while True:
             time.sleep(1)
             f = open('/home/pi/Desktop/smartcane/blackbox/flag.txt','r')
             flag = f.read()
             print(flag)
             currenttime = int(time.time())
             
             if currenttime-int(starttime) == 60:
               camera.stop_preview()
               camera.stop_recording()
               f.close()
               os.system('MP4Box -add /home/pi/Desktop/smartcane/blackbox/'+starttime+'.h264 /home/pi/Desktop/smartcane/blackbox/'+starttime+'.mp4') 
               os.system('rm '+starttime+'.h264')
               break
              
             if flag=='0':
               camera.stop_preview()
               camera.stop_recording()
               f.close()
               os.system('MP4Box -add /home/pi/Desktop/smartcane/blackbox/'+starttime+'.h264 /home/pi/Desktop/smartcane/blackbox/'+starttime+'.mp4') 
               os.system('rm '+starttime+'.h264')
               break
    
    
    
    
    