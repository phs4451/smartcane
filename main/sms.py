# -*- coding: utf-8 -*-
import os
import time
import gps
import sys
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
import picamera
from picamera.array import PiRGBArray
import requests
from collections import OrderedDict
import pprint
from PIL import Image
import record
import flag

##  @brief This sample code demonstrate how to send sms through CoolSMS Rest API PHP
def main():
    
    print("sms hi")
    os.system('gpspipe -r -d -l -o /home/pi/smartcane/sms/date1.txt')
    # set api key, api secret
    api_key = "NCS4QACAQPBEDUMG"
    api_secret = "XBGIKE2OTK0SJEDL86QTWXXQXYUMHBNU"
    
    imgname='./image.jpg'
    camera = picamera.PiCamera()
    camera.vflip=True
    camera.hflip=True
    os.system("mplayer voicefile/camera.mp3")
    capture = PiRGBArray(camera)
    camera.capture(capture,format='rgb',use_video_port=True)
    capture = Image.fromarray(capture.array)
    capture.save(imgname)
    camera.close()

    #flag.initFlag()
    
    
    time.sleep(10)
    params = dict()
    
    if gps.convert('date1.txt') == 1:
      params['type'] = 'mms' # Message type ( sms, lms, mms, ata )
      params['to'] = '010-6473-4451'
      params['from'] = '01064734451'
      params['text'] = 'http://maps.google.com/maps?z=11&t=k&q=37.558088+126.998222'
      params["image"] = imgname # image for MMS. type must be set as "MMS"
    else:
      latresult,longresult = gps.convert('date1.txt')
      params['type'] = 'mms' # Message type ( sms, lms, mms, ata )
      params['to'] = '010-6473-4451'
      params['from'] = '01064734451'
      params['text'] = 'http://maps.google.com/maps?z=11&t=k&q=' + latresult +'+'+longresult # Message   
      params["image"] = imgname # image for MMS. type must be set as "MMS" 
    ## 4 params(to, from, type, text) are mandat?ory. must be filled
    
    cool = Message(api_key, api_secret)
    
    try:
        
        response = cool.send(params)
    
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID : %s" % response['group_id'])
    
        os.system("mplayer /home/pi/Desktop/smartcane/voicefile/mms.MP3")
       
        if "error_list" in response:
            print("Error List : %s" % response['error_list'])
            
          

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)


    sys.exit()
