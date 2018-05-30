# -*- coding: utf-8 -*- 
import picamera
from picamera.array import PiRGBArray
import time
import requests
import base64
import json
from collections import OrderedDict
import pprint
from PIL import Image

def encode_img(img):
	with open(img,'rb') as imgfile:
		encoded_img = base64.encodestring(imgfile.read())
	return encoded_img.decode()

def send_img(img,ip):
	data = {'image':img}
	Jsondata = json.dumps(data)
	response = requests.post(ip,Jsondata)
	result = response.content.decode('utf-8').split('\r\n')
	temp =json.loads(result[5])
	if(temp['result'] is not ''):
		print(temp['result'])
	else:
		print('오류 발생 - 파싱')

def main():
    
    server_ip = 'http://210.94.185.47:30010'
    imgname='./image.jpg'
    
    camera = picamera.PiCamera()
    camera.vflip=True
    camera.hflip=True
    rawCapture = PiRGBArray(camera)
    
    camera.capture(rawCapture,format='rgb',use_video_port=True)
    capture = Image.fromarray(rawCapture.array)
    rawCapture.truncate(0)
    capture.save(imgname)
    temp = encode_img(imgname)
    #print(temp)
    send_img(temp,server_ip)
    camera.close()



