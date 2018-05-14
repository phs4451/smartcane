import time
import RPi.GPIO as GPIO
import os
import datetime as dt
import picamera


def recording():
      
      starttime = str(int(time.time()))
      
      filename = '/home/pi/Desktop/smartcane/blackbox/record/'+starttime+'.h264'
 
      with picamera.PiCamera() as camera:
             camera.start_preview()
             camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
             camera.start_recording(filename) 
             
             while True:
                f = open("/home/pi/Desktop/smartcane/blackbox/flag.txt",'r')
                flag = f.readline()
                print(flag)
                time.sleep(1)
                currenttime = int(time.time())
                
                if currenttime-int(starttime) == 25:
                  camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                  camera.stop_preview()
                  camera.stop_recording()
                  camera.close()
                  f.close()
                  os.system('MP4Box -add '+filename+' /home/pi/Desktop/smartcane/blackbox/record/'+starttime+'.mp4')
                  os.system('rm /home/pi/Desktop/smartcane/blackbox/record/'+starttime+'.h264')
                  recording()
                  break
                  
                
                if flag=='0':
                    camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    camera.stop_preview()
                    camera.stop_recording()
                    camera.close()
                    f.close()
                    os.system('MP4Box -add /home/pi/Desktop/smartcane/blackbox/record/'+starttime+'.h264 /home/pi/Desktop/smartcane/blackbox/record/'+starttime+'.mp4') 
                    os.system('rm /home/pi/Desktop/smartcane/blackbox/record/'+starttime+'.h264')
                    break

                  
                  
               
                  
              
                  
    
