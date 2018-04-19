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




##  @brief This sample code demonstrate how to send sms through CoolSMS Rest API PHP
if __name__ == "__main__":
    # set api key, api secret
    api_key = "NCS4QACAQPBEDUMG"
    api_secret = "WDCC4SGGH9HRBIRFV4EVZEJGL3HBUF1O"
    
    imgname='./image.jpg'
    camera = picamera.PiCamera()
    capture = PiRGBArray(camera)
    
    camera.capture(capture,format='rgb',use_video_port=True)
    capture = Image.fromarray(capture.array)
    capture.save(imgname)
    camera.close()
    
    os.system('gpspipe -r -d -l -o /home/pi/smartcane/sms/date1.txt')
    time.sleep(10)

    params = dict()
    
    if gps.convert('date1.txt') == 1:
      params['type'] = 'mms' # Message type ( sms, lms, mms, ata )
      params['to'] = '01079128566' # Recipients Number '01000000000,01000000001'
      params['from'] = '01064734451' # Sender number
      params['text'] = 'Location ERROR!!'# Message
      params["image"] = "../sms/image.jpg" # image for MMS. type must be set as "MMS"
    else:
      latresult,longresult = gps.convert('date1.txt')
      params['type'] = 'mms' # Message type ( sms, lms, mms, ata )
      params['to'] = '01079128566' # Recipients Number '01000000000,01000000001'
      params['from'] = '01064734451' # Sender number
      params['text'] = 'http://maps.google.com/maps?z=11&t=k&q=' + latresult + longresult # Message   
      params["image"] = "../sms/image.jpg" # image for MMS. type must be set as "MMS" 
    ## 4 params(to, from, type, text) are mandat?ory. must be filled
    
    
    
    cool = Message(api_key, api_secret)
    
    try:
        
        response = cool.send(params)
        
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID : %s" % response['group_id'])

        if "error_list" in response:
            print("Error List : %s" % response['error_list'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

    sys.exit()
