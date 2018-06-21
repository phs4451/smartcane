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
import os
import tts
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
    sentence = ''
    if(temp['result'] != 'nothing'):
        sentence = make_sentence(temp['result'])
        tts.tts_Clova(text = sentence)
    else:
        os.system('mplayer  voicefile/noobjectfound.mp3')
        print('parsing error')

def main():
    server_ip = 'http://210.94.185.47:30010'
    imgname='./image.jpg'
    camera = picamera.PiCamera()
    camera.vflip=True
    camera.hflip=True
    os.system("mplayer voicefile/camera.mp3")
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture,format='rgb',use_video_port=True)
    capture = Image.fromarray(rawCapture.array)
    rawCapture.truncate(0)
    capture.save(imgname)
    temp = encode_img(imgname)
    #print(temp)
    send_img(temp,server_ip)
    camera.close()


def make_sentence(items):
    name_file = open('list.txt','r')
    name_list = []
    while True:
        line = name_file.readline()
        if not line: break
        name_list.append(line.split('#'))
    name_file.close()
    
    items = items.split('#')
    items_split = []
    for item in items:
        items_split.append(item.split(','))
    result_list = []
    for item in items_split:
        for name in name_list:
            if name[0] == item[0]:
                result_list.append(name[1]+' '+item[1]+name[2])
                break
    #print(result_list)
    result_sen = ''
    for result in result_list:
        if result != result_list[-1]:
            result_sen += result + ', '
        else:
            result_sen += result
    print(result_sen)
    return result_sen
