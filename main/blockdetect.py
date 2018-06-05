#-*- coding: utf-8 -*-
import cv2
import numpy as np
from wand.image import Image as Img
import picamera
from picamera.array import PiRGBArray
from PIL import Image
import flag
import os

dirname = './block_result'
if not os.path.exists(dirname):
    os.makedirs(dirname)

target = os.path.join(dirname,"white4.jpg")

row = 1
col = 1

areas = [] 
cnt = 0 
#def adjust_gamma(image, gamma=1.0):

   #invGamma = 1.0 / gamma
   #table = np.array([((i / 255.0) ** invGamma) * 255
      #for i in np.arange(0, 256)]).astype("uint8")

   #return cv2.LUT(image, table)

def detect(c,img):
        
        
        shape = "unidentified"
        peri = cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c, 0.005*peri, True) # smooth edge
        (x, y, w, h) = cv2.boundingRect(approx)
        
        
        #일정 크기 이상의 모양만 식별
        if (10 < w < 1500 and 10 < h < 1500):
            #이 부분은 고민 후 수정
            if (len(approx) == 3 or len(approx) == 4 or len(approx) == 5 ):
                cv2.drawContours(img, [approx],  -1, (0, 0, 255), 2)
                areas.append((cv2.contourArea(c),x,y,w,h))
                print('w = ' + str(w) + '\th = ' + str(h)+'\tx = ' + str(x) + '\ty = ' + str(y) )
                
            else:
                #cv2.drawContours(img, [approx],  -1, (0, 0, 255), 2)
                print( "Not block" )
        
def cutImage():
    #hi = cv2. imread(target)
    #target1 = cv2.resize(hi, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_AREA)
    #cv2.imwrite('target1.jpg',target1)   
    #폰 사진 축소용...... 바로 아래 target -> 'target1.jpg' 로 해주면 됨
    
    with Img(filename = target) as image:

        cropHeight = int(image.height/row) 
        cropWidth = int(image.width/col)
  
        for i in range(0, row): 
            for j in range(0, col): 
              left = j*cropWidth
              right = (j+1)*cropWidth
              top = i*cropHeight
              bottom = (i+1)*cropHeight
              
              with image[left:right, top:bottom] as newimage:
                print("new : {0} , {1}".format(newimage.format, newimage.size))
                newimage.save(filename=os.path.join(dirname,"{0}x{1}_{2}".format(i, j, "cutresult.jpg")))


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
    
    #flag.initFlag()
    cutImage()

    cutimg = [[0 for i in range(row)] for j in range(col)]
    
    
    for i in range(0, row): 
        for j in range(0, col): 

            # 가우시안 필터 처리
            cutimg[i][j]  = cv2.imread(os.path.join(dirname,"{0}x{1}_{2}".format(i, j, "cutresult.jpg")))
            blur = cv2.GaussianBlur(cutimg[i][j],(3,3),0)
            blurfilename = os.path.join(dirname,'blur.jpg')
            cv2.imwrite(blurfilename,blur)
            frame = cv2.imread(blurfilename)
            
            #CLAHE
            #image_lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            #l_channel, a_channel, b_channel = cv2.split(image_lab)
            #clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(8, 8))
            #cl = clahe.apply(l_channel)
            #merged_channels = cv2.merge((cl, a_channel, b_channel))
            #final_image = cv2.cvtColor(merged_channels, cv2.COLOR_LAB2BGR)
            
            
            #gamma correction 명암 조절
            #gamma = 1.5
            #adjusted = adjust_gamma(frame, gamma=gamma)
            #cv2.imwrite('adjusted.jpg',adjusted)
            
            #hsv변환
            img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  

            img_h, img_s, img_v = cv2.split(img_hsv)
            

            #노란색 범위 지정
            lower_yellow = np.array([0,0,170])
            upper_yellow = np.array([180,20,255]) 

            mask = cv2.inRange(img_hsv, lower_yellow, upper_yellow)    

            # Bitwise-AND mask and original image  
            img_result = cv2.bitwise_and(frame,frame, mask= mask)
            img_yellow_name = os.path.join(dirname,'img_yellow.jpg')
            cv2.imwrite( img_yellow_name, img_result ) 

            img = cv2.imread(img_yellow_name)
            imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            #Thresholding
            ret, thr = cv2.threshold(imgray, 20, 255, 0)
            #thr = cv2.adaptiveThreshold(imgray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,15,2)
            _, contours, _ = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            #thr = cv2.adaptiveThreshold(frame,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,15,2)

            for con in contours:
                detect(con,img)
                
            areas_sorted = sorted(areas, key=lambda area: area[0], reverse =True)
            print(areas_sorted)
           
            img_detect_name = os.path.join(dirname,str(i) +'x'+str( j) +'_detect.jpg')
            cv2.imwrite(img_detect_name, img)
    
    img1_name = os.path.join(dirname,'0x0_cutresult.jpg')
    img2_name = os.path.join(dirname,'0x0_detect.jpg')
    temp =cv2.imread(img1_name)
    temp2 =cv2.imread(img2_name)
    for i,area in enumerate(areas_sorted):
                print(i,area[1],area[2])
                cv2.putText(temp2,str(i),(area[1],area[2]),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(255,255,255))
    cv2.imshow('original',temp)
    cv2.imshow('detect',temp2)
    #cv2.imshow('thr',thr)
    #cv2.imshow('clahe',final_image)
    #cv2.imshow('ad',adjusted)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

