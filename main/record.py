import time
import RPi.GPIO as GPIO
import os
import datetime as dt
import picamera
from operator import eq
import flag
import oscheck

cmd = 'MP4Box add ~.h264 !.mp4'

folder_name ='./record/'
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

def recording():
 
      with picamera.PiCamera() as camera:
             camera.vflip=True
             camera.hflip=True
             camera.resolution = (400,300)
             #filename = '/home/pi/Desktop/smartcane/blackbox/record/'+starttime+'.h264'
             #camera.start_preview()
             #camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
             #camera.start_recording(filename) 
             realstarttime = 1
             while True:
                fl = flag.getFlag()#f.readline()
                #print(fl)
                time.sleep(0.01)
                currenttime = int(time.time())

                if currenttime-int(realstarttime) == 25:
                    
                    camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    camera.stop_preview()
                    camera.stop_recording()
                    realstarttime = 1
                    #oscheck.getDirSize('/home/pi/Desktop/smartcane/blackbox/record')

                  
                elif fl=='0':
                    try:
                        camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        camera.stop_preview()
                        camera.stop_recording()
                        camera.close()
                        realstarttime = 1

                    except picamera.PiCameraError:
                        continue
                    
                elif fl=='1':
                    try:
                        camera.start_preview()
                        camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        starttime = str(int(time.time()))
                        filename = os.path.join(folder_name,starttime+'.h264')
                        camera.start_recording(filename) 
                        realstarttime = starttime
                        #print('first')
                    except picamera.PiCameraAlreadyRecording as hi:
                        #print(type(hi))
                        #print('already')
                        continue
                    except picamera.PiCameraClosed:
                        camera = picamera.PiCamera()
                            
            
                            
                            
                        
    
