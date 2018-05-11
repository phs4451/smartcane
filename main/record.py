import time
import picamera
import RPi.GPIO as GPIO
import os
import datetime as dt


def recording(main_camera):
      print(main_camera)
      global flag
      flag=2

      starttime = str(int(time.time()))
      
      filename = '/home/pi/Desktop/smartcane/blackbox/record/'+starttime+'.h264'
      

      with main_camera as camera:
             camera.start_preview()
             camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
             camera.start_recording(filename)   
             
             
      
             while True:
                camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                time.sleep(1)
                print(flag)
                currenttime = int(time.time())
                
                if currenttime-int(starttime) == 10:
                  camera.stop_preview()
                  camera.stop_recording()
                  camera.close()
                  os.system('MP4Box -add '+filename+' /home/pi/Desktop/smartcane/blackbox/record/'+starttime+'.mp4')
                  os.system('rm /home/pi/Desktop/smartcane/blackbox/record/'+starttime+'.h264')
                  break
                
                if flag==0:
                  camera.stop_preview()
                  camera.stop_recording()
                  camera.close()
                  os.system('MP4Box -add /home/pi/Desktop/smartcane/blackbox/record/'+starttime+'.h264 /home/pi/Desktop/smartcane/blackbox/record/'+starttime+'.mp4') 
                  os.system('rm /home/pi/Desktop/smartcane/blackbox/record/'+starttime+'.h264')
                  break
              
                
              
                  
    
