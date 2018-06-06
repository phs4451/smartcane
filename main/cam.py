import picamera
from picamera.array import PiRGBArray
import time
from PIL import Image

imgname=str(time.time())+'.jpg'
camera = picamera.PiCamera()
camera.vflip=True
camera.hflip=True
time.sleep(1.5)
capture = PiRGBArray(camera)
camera.capture(capture,format='rgb',use_video_port=True)
capture = Image.fromarray(capture.array)
capture.save(imgname)
camera.close()
