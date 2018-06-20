#-*- coding: utf-8 -*-
import cv2
import numpy as np
from wand.image import Image as Img
import picamera
from picamera.array import PiRGBArray
from PIL import Image
import flag
import os
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
import time
import math
import tts

dirname = './block_result'
if not os.path.exists(dirname):
    os.makedirs(dirname)

target = os.path.join(dirname,"represent1.jpg")  #white4, white16,  white17, white18, white19

rectangles = [] 
cnt = 0

width = 800
height = 600

def getDirection(degree):
    if degree < 0:
        degree = 90 + degree
        if  0 <= degree < 10:
            return  "12"
        elif 15 <= degree <= 45:
            return "13"
        elif 45 < degree <= 90:
            return "14"
    else:
        degree = 90 - degree
        if  0 <= degree < 10:
            return "12"
        elif 15 <= degree <= 45:
            return "11"
        elif 45 < degree <= 90:
            return  "10"
    


    
def avgHSV(img_v):
    
    c_img_v = img_v.tolist()
    
    sum = 0
    avg = 0
    
    for i in range(height):
        for j in range(width):
            sum = sum + c_img_v[i][j]
            
    avg = sum / (width*height)
            
    return avg
    
   
def order_points(pts):
    coords = np.zeros((4,2), dtype = "float32")
    s= pts.sum(axis = 1)
    
    coords[0] = pts[np.argmin(s)]
    coords[2] = pts[np.argmax(s)]
    
    diff = np.diff(pts, axis = 1)
    
    if(np.argmax(s)==np.argmin(diff)):
        pts[np.argmin(diff)]=0
        diff2 = np.diff(pts, axis = 1)
        coords[1] = pts[np.argmin(diff2)]
    else:
        coords[1] = pts[np.argmin(diff)]
    coords[3] = pts[np.argmax(diff)]
    
    return coords
    

def detect(c,img):
        
        peri = cv2.arcLength(c,True)
        
        approx = cv2.approxPolyDP(c, 0.01*peri, True) # smooth edge
        area = cv2.contourArea(c)
        
        if (len(approx)==4 ) and area >= 1050:            
            cv2.drawContours(img, [approx],  -1, (0, 0, 255), 3)
            temp_approx = approx.reshape(len(approx),2)
            #print(area, approx)
            rect = order_points(temp_approx)
            #if rect[0][0] != 0 and rect[1][0] !=0 and rect[2][0]!=0 and rect[3][0] != 0:
            rectangles.append((area,rect))
        #elif area>260:
            #cv2.drawContours(img, [approx],  -1, (0, 0, 255), 2)
            #print( "Not block" )
def linear_reg(x_data,y_data):
    x_data =np.array(x_data)
    y_data =np.array(y_data)
    gradient, intercept, r_value,p_value,std_err = stats.linregress(x_data,y_data)
    gradient=round(gradient,2)
    intercept=round(intercept,2)
    return gradient,intercept
    
def draw_line(img,gradient,intercept,index):
    if index==1:
        color = (255,0,0)
    elif index==2: 
        color = (0,255,0)
    elif index==3:
        color =(0,0,255)
    height,width,channel = img.shape
    y1=0
    x1=((y1-intercept)/gradient).astype(int)
    y2=height
    x2=((y2-intercept)/gradient).astype(int)
    cv2.line(img,(x1,y1),(x2,y2),color,3)
    return img

#main
def main():
    imgname=os.path.join(dirname,'blockimage.jpg')
    camera = picamera.PiCamera()
    camera.vflip=True
    camera.hflip=True
    os.system("mplayer voicefile/camera.mp3")
    capture = PiRGBArray(camera)
    camera.capture(capture,format='rgb',use_video_port=True)
    capture = Image.fromarray(capture.array)
    capture.save(imgname)
    camera.close()
    
    img = cv2.imread(target)
    img = cv2.resize(img, (width,height), interpolation=cv2.INTER_AREA)
    blur = cv2.GaussianBlur(img,(3,3),0)
    blurfilename = os.path.join(dirname,'blur.jpg')
    cv2.imwrite(blurfilename,blur)
    frame = cv2.imread(blurfilename)
    

    #hsv??
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  

    img_h, img_s, img_v = cv2.split(img_hsv)
    
    avgValue = int(avgHSV(img_v))

    #??? ?? ??

    lower_white = np.array([0,0,avgValue+45])
    upper_white = np.array([180,20,255]) 
    
    mask = cv2.inRange(img_hsv, lower_white, upper_white)

    # Bitwise-AND mask and original image  
    img_result = cv2.bitwise_and(frame,frame, mask= mask)
    img_yellow_name = os.path.join(dirname,'img_yellow.jpg')
    cv2.imwrite( img_yellow_name, img_result ) 
            
    img = cv2.imread(img_yellow_name)
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #dilation
    kernel = np.ones((6, 6), np.uint8)
    dilation = cv2.dilate(imgray, kernel, iterations=1)
 
    #opening
    kernel = np.ones((7, 7), np.uint8)
    opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN,kernel)

    #Thresholding
    ret, thr = cv2.threshold(opening, 20, 255, 0)
    
    cv2.imshow('dddd',thr)

    _, contours, _ = cv2.findContours(thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    

    for con in contours:
        detect(con,img)
    
    #??? ?? ?? ?? ??
    rectangle_sorted = sorted(rectangles, key=lambda area: area[0], reverse =True)
    
    img_detect_name = os.path.join(dirname,'detectimg.jpg')
    cv2.imwrite(img_detect_name, img)
            
    img1_name = os.path.join(target)
    img2_name = os.path.join(dirname,'detectimg.jpg')
    img_original =cv2.imread(img1_name)
    img_original = cv2.resize(img_original,(width,height) , interpolation=cv2.INTER_AREA)
    img_detect =cv2.imread(img2_name)
    x_list=[]
    y_list=[]
    x2_list=[] 
    y2_list=[]
    for i,rect in enumerate(rectangle_sorted):
        ##rect is composed of size of rectangle(index 0) and 4 coords(index 2)
        for j in range(len(rect[1])):
            cv2.putText(img_detect,str(j),(rect[1][j][0],rect[1][j][1]),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(255,255,255))
        if rect[1][0][0]!=0:
            x_list.append(rect[1][0][0])
            y_list.append(rect[1][0][1])
            x2_list.append(rect[1][2][0])
            y2_list.append(rect[1][2][1])
        else:
            x_list.append(rect[1][0][0])
            y_list.append(rect[1][0][1])
            x2_list.append(rect[1][2][0])
            y2_list.append(rect[1][2][1])
    
        
    if len(x_list) != 0:
        gradient1=0;intercept1=0
        gradient2=0;intercept2=0
        
        gradient1, intercept1 = linear_reg(x_list,y_list)
        gradient2, intercept2 = linear_reg(x2_list,y2_list)
        
        x_intersect = (intercept2-intercept1)/(gradient1-gradient2)
        y_interscet = x_intersect*gradient1+intercept1
        y_mid = 500
        x_mid = y_mid*(gradient1+gradient2)-(intercept1*gradient2) - (gradient1*intercept2)
        x_mid /=2*gradient1*gradient2
        
        x_third = [x_intersect,x_mid]
        y_third = [y_interscet,y_mid]
        gradient3,intercept3 = linear_reg(x_third,y_third)
        
        if not np.isnan(gradient1):
            if not np.isnan(gradient2):
                img_detect = draw_line(img_detect,gradient1,intercept1,1)
                img_detect = draw_line(img_detect,gradient2,intercept2,2)
                img_detect = draw_line(img_detect,gradient3,intercept3,3)
                print(gradient1,gradient2)
        if not np.isnan(gradient3):
            degree = int(math.degrees(math.atan(gradient3)))
        
        direction_result = "mplayer voicefile/"+getDirection(degree)+"_clockwise.mp3"
        os.system(direction_result)
        
        print(direction_result)
        
    
        #if gradient1 >0 and gradient2>0:
            #print("Left side")
            #os.system("mplayer voicefile/left.mp3")
        #elif gradient1 <0 and gradient2>0:
            #print("Center")
            #os.system("mplayer voicefile/front.mp3")
        #elif gradient1 <0 and gradient2<0:
            #print("Right side")
            #os.system("mplayer voicefile/right.mp3")
    else:
        print("NO CROSSWALK")
        os.system("mplayer voicefile/nodetect.mp3")

    cv2.imshow('original',img_original)
    cv2.imshow('detect',img_detect)
    cv2.imwrite('detectimg.jpg',img_detect)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

