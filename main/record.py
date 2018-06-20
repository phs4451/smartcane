import time
import RPi.GPIO as GPIO
import os
import datetime as dt
import picamera
from operator import eq
import flag
import oscheck

folder_name ='./record/'
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

def recording():
 
      with picamera.PiCamera() as camera:

             realstarttime = 1
             
             while True:
                fl = flag.getFlag(flag.camera)
                
                time.sleep(0.01)
                currenttime = int(time.time())

                if currenttime-int(realstarttime) == 25:
                    
                    camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    #camera.stop_preview()
                    camera.stop_recording()
                    realstarttime = 1
                    oscheck.getDirSize('/home/pi/Desktop/smartcane/main/record')

                  
                elif fl=='0':
                    try:
                        camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        #camera.stop_preview()
                        camera.stop_recording()
                        camera.close()
                        realstarttime = 1
                        oscheck.getDirSize('/home/pi/Desktop/smartcane/main/record')

                    except picamera.PiCameraError:
                        continue
                    
                elif fl=='1':
                    try:
                        camera.vflip=True
                        camera.hflip=True
                        camera.resolution = (400,300)
                        
                        #camera.start_preview()
                        camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        starttime = str(int(time.time()))
                        filename = os.path.join(folder_name,starttime+'.h264')
                        camera.start_recording(filename) 
                        realstarttime = starttime
                        
                    except picamera.PiCameraAlreadyRecording as hi:
    
                        continue
                    except picamera.PiCameraClosed:
                        camera = picamera.PiCamera()
                    except picamera.PiCameraRuntimeError:
                        continue
                            
            
                            
                            
                        
    
