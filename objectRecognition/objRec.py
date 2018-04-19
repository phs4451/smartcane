import picamera
from picamera.array import PiRGBArray
import time
import requests
import base64
import json
from collections import OrderedDict
import pprint
from PIL import Image


server_ip = 'http://210.94.185.47:30010'
imgname='./image.jpg'
camera = picamera.PiCamera()
rawCapture = PiRGBArray(camera)


def encode_img(img):
	with open(img,'rb') as imgfile:
		encoded_img = base64.encodestring(imgfile.read())
	return encoded_img.decode()

def send_img(img,ip):
	data = {'image':img}
	Jsondata = json.dumps(data)
	response = requests.post(ip,Jsondata)
	#print(response.text)
	temp = response.headers
	#print(type(temp))
	print(response.headers['content-type'])
    
def objRecognition(camera,rawCapture,imgname,server_ip):
    camera.capture(rawCapture,format='rgb',use_video_port=True)
    capture = Image.fromarray(rawCapture.array)
    rawCapture.truncate(0)
    capture.save(imgname)
    temp = encode_img(imgname)
    print(temp)
    send_img(temp,server_ip)



