import psycopg2
import urllib
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import argparse
import re
import cgi
import json
import datetime
import re
import json
import base64
import binascii
import os
import pydarknet
import cv2
import sys
import time

class LocalData(object):
    records= {}
class MyHandler(BaseHTTPRequestHandler):

    myID = 10
    device_id = 0

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.myID = self.myID +1

    #def do_GET(self):
        

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        input_path = 'myresult/test.jpg'
        dirname = './myresult'
        print("post start ")
        self._set_headers()
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

        data = json.loads(self.data_string)
        
        fp = open(input_path,'wb')
        temp = data['image'].encode()
        temp2 = base64.decodestring(temp)
        fp.write(temp2)
        fp.close()
        
        if not os.path.isfile(input_path):
            print('Saving Error ',input_path)
            time.sleep(0.5)
        else:
            ext = os.path.splitext(input_path)[1]
            ext = ext.lower()
            img = cv2.imread(input_path)
            ret = pydarknet.detect_image(img)
            
            obj_list = list()
            for i in ret:
                obj_list.append(i[0])            
            obj_list = sorted(obj_list)

            obj_count = {}
            result_text = ''
            
            if len(obj_list) != 0:
                for obj in obj_list:
                    try: obj_count[obj]+=1
                    except: obj_count[obj]=1
                print(obj_count)
                for key in obj_count.keys():
                    result_text += key+','+str(obj_count[key])+'#'
            else:
                result_text = "nothing"

            img = pydarknet.draw_dets(img, ret, text='100')
            outfile = os.path.splitext(input_path)[0] + '_detect' + ext
            cv2.imwrite(outfile, img)
            
        result = {'result':result_text,'num':len(ret)}
        result = json.dumps(result)
        self.send_response(200)
        self.send_header('content-type','text/json')
        data = {'result':result_text}
        self.end_headers()
        self.wfile.write(json.dumps(data))
        
	
def main():
    pydarknet.load("cfg/yolo.cfg", "yolo.weights")
    try:
        dirname = './from_post'
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        server = HTTPServer(("",30010), MyHandler)
        print ('Welcome to the machine')
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()

if __name__== '__main__':
    main()
        



