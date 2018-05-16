import time
import RPi.GPIO as GPIO
import os
import datetime as dt
import picamera


def recording():
      
      
 
      with picamera.PiCamera() as camera:
             
             #filename = '/home/pi/Desktop/smartcane/blackbox/record/'+starttime+'.h264'
             #camera.start_preview()
             #camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
             #camera.start_recording(filename) 
             realstarttime = 1
             while True:
                f = open("/home/pi/Desktop/smartcane/blackbox/flag.txt",'r')
                flag = f.readline()
                print(flag)
                time.sleep(1)
                currenttime = int(time.time())

                if currenttime-int(realstarttime) == 25:
                  camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                  camera.stop_preview()
                  camera.stop_recording()
                  f.close()
                  os.system('MP4Box -add '+'/home/pi/Desktop/smartcane/blackbox/record/'+realstarttime+'.h264'+' /home/pi/Desktop/smartcane/blackbox/record/'+realstarttime+'.mp4')
                  os.system('rm /home/pi/Desktop/smartcane/blackbox/record/'+realstarttime+'.h264')
                  
                  
                elif flag=='0':
                    try:
                        camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        camera.stop_preview()
                        camera.stop_recording()
        
                        f.close()
                        os.system('MP4Box -add /home/pi/Desktop/smartcane/blackbox/record/'+realstarttime+'.h264 /home/pi/Desktop/smartcane/blackbox/record/'+realstarttime+'.mp4') 
                        os.system('rm /home/pi/Desktop/smartcane/blackbox/record/'+realstarttime+'.h264')
                        
                    except picamera.PiCameraError:
                        continue
                    
                elif flag=='2':
                    try:
                        camera.start_preview()
                        camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        starttime = str(int(time.time()))
                        filename = '/home/pi/Desktop/smartcane/blackbox/record/'+starttime+'.h264'
                        camera.start_recording(filename) 
                        realstarttime = starttime
                        print('first')
                    except picamera.PiCameraError:
                        print('already')
                        continue
                        
    
