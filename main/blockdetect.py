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

dirname = './block_result'
if not os.path.exists(dirname):
    os.makedirs(dirname)

target = os.path.join(dirname,"white12.jpg")

rectangles = [] 
cnt = 0
   
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
        
        approx = cv2.approxPolyDP(c, 0.0044*peri, True) # smooth edge
        area = cv2.contourArea(c)
        
        if (len(approx)==4 ) and area >= 500:            
            cv2.drawContours(img, [approx],  -1, (0, 0, 255), 2)
            temp_approx = approx.reshape(len(approx),2)
            print(area, approx)
            rect = order_points(temp_approx)
            if rect[0][0] != 0 and rect[1][0] !=0 and rect[2][0]!=0 and rect[3][0] != 0:
                rectangles.append((area,rect))
        elif area>260:
            #cv2.drawContours(img, [approx],  -1, (0, 0, 255), 2)
            print( "Not block" )
def linear_reg(x_data,y_data):
    x_data =np.array(x_data)
    y_data =np.array(y_data)
    gradient, intercept, r_value,p_value,std_err = stats.linregress(x_data,y_data)
    gradient=round(gradient,2)
    intercept=round(intercept,2)
    return gradient,intercept
    
def draw_line(img,gradient,intercept):
    height,width,channel = img.shape
    y1=0
    x1=((y1-intercept)/gradient).astype(int)
    y2=height
    x2=((y2-intercept)/gradient).astype(int)
    cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)
    return img

#main
def main():
    imgname=os.path.join(dirname,'blockimage.jpg')
    camera = picamera.PiCamera()
    camera.vflip=True
    camera.hflip=True
    capture = PiRGBArray(camera)
    
    camera.capture(capture,format='rgb',use_video_port=True)
    capture = Image.fromarray(capture.array)
    capture.save(imgname)
    camera.close()
    
    img = cv2.imread(target)
    #img = cv2.resize(img, None, fx=0.4, fy=0.4, interpolation=cv2.INTER_AREA)
    blur = cv2.GaussianBlur(img,(3,3),0)
    blurfilename = os.path.join(dirname,'blur.jpg')
    cv2.imwrite(blurfilename,blur)
    frame = cv2.imread(blurfilename)
    
    #hsv??
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  

    img_h, img_s, img_v = cv2.split(img_hsv)
    
    #??? ?? ??
    lower_white = np.array([0,0,230])
    upper_white = np.array([180,20,255]) 
    
    mask = cv2.inRange(img_hsv, lower_white, upper_white)

    # Bitwise-AND mask and original image  
    img_result = cv2.bitwise_and(frame,frame, mask= mask)
    img_yellow_name = os.path.join(dirname,'img_yellow.jpg')
    cv2.imwrite( img_yellow_name, img_result ) 
            
    img = cv2.imread(img_yellow_name)
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Thresholding
    ret, thr = cv2.threshold(imgray, 20, 255, 0)

    _, contours, _ = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    #thr = cv2.adaptiveThreshold(frame,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,15,2)

    for con in contours:
        detect(con,img)
    
    #??? ?? ?? ?? ??
    rectangle_sorted = sorted(rectangles, key=lambda area: area[0], reverse =True)
    
    img_detect_name = os.path.join(dirname,'detectimg.jpg')
    cv2.imwrite(img_detect_name, img)
            
    img1_name = os.path.join(target)
    img2_name = os.path.join(dirname,'detectimg.jpg')
    img_original =cv2.imread(img1_name)
    #img_original = cv2.resize(img_original, None, fx=0.4, fy=0.4, interpolation=cv2.INTER_AREA)
    img_detect =cv2.imread(img2_name)
    x_list=[]
    y_list=[]
    x2_list=[] 
    y2_list=[]
    for i,rect in enumerate(rectangle_sorted):
        ##rect is composed of size of rectangle(index 0) and 4 coords(index 2)
        for j in range(len(rect[1])):
            cv2.putText(img_detect,str(j),(rect[1][j][0],rect[1][j][1]),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(0,255,255))
        if rect[1][0][0]!=0:
                x_list.append(rect[1][0][0])
                y_list.append(rect[1][0][1])
                x2_list.append(rect[1][2][0])
                y2_list.append(rect[1][2][1])
    if len(x_list) != 0:
        gradient1, intercept1 = linear_reg(x_list,y_list)
        img_detect = draw_line(img_detect,gradient1,intercept1)
        gradient2, intercept2 = linear_reg(x2_list,y2_list)
        img_detect = draw_line(img_detect,gradient2,intercept2)
        print(gradient1,gradient2)
        if gradient1 >0 and gradient2>0:
            print("Right side")
        elif gradient1 <0 and gradient2>0:
            print("Center")
        elif gradient1 <0 and gradient2<0:
            print("Left side")
    else:
        print("NO CROSSWALK")
    
    cv2.imshow('original',img_original)
    cv2.imshow('detect',img_detect)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

