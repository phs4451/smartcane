#-*- coding: utf-8 -*-
import cv2
import numpy as np
from wand.image import Image


target = "yel3.jpg"

row = 3
col = 3

def detect(c):
        shape = "unidentified"
        peri = cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c, 0.015*peri, True) # smooth edge
        (x, y, w, h) = cv2.boundingRect(approx)
        print('w = ' + str(w) + '\th = ' + str(h) )
        
        #일정 크기 이상의 모양만 식별
        if (40 < w < 500 and 40 < h < 500):
            #이 부분은 고민 후 수정
            if len(approx) == 3:
                shape = "triangle"
                cv2.drawContours(img, [approx],  -1, (255, 0, 0), 2)
            elif len(approx) == 4:
                shape = "rectangle"
                cv2.drawContours(img, [approx],  -1, (0, 0, 255), 2)
            elif len(approx) == 5:
                shape = "pentagon"
                cv2.drawContours(img, [approx],  -1, (0, 255, 0), 2)
            else:
                cv2.drawContours(img, [approx],  -1, (255, 0, 255), 2)
                shape = "???"
            
        return shape
    
def cutImage():
    #hi = cv2. imread(target)
    #target1 = cv2.resize(hi, None, fx=0.4, fy=0.4, interpolation=cv2.INTER_AREA)
    #cv2.imwrite('target1.jpg',target1)   
    #폰 사진 축소용...... 바로 아래 target -> 'target1.jpg' 로 해주면 됨
    
    with Image(filename = target) as image:

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
                newimage.save(filename="{0}x{1}_{2}".format(i, j, "cutresult.jpg"))


#main
cutImage()

cutimg = [[0 for i in range(row)] for j in range(col)]

for i in range(0, row): 
    for j in range(0, col): 
        # 가우시안 필터 처리
        cutimg[i][j]  = cv2.imread(filename="{0}x{1}_{2}".format(i, j, "cutresult.jpg"))
        blur = cv2.GaussianBlur(cutimg[i][j],(3,3),0)
        cv2.imwrite("blur.jpg",blur)

        frame = cv2.imread('blur.jpg')
        img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  

        img_h, img_s, img_v = cv2.split(img_hsv)

	    #노란색 범위 지정
        lower_blue = np.array([10,100,100])  
        upper_blue = np.array([30,255,255])  

        mask = cv2.inRange(img_hsv, lower_blue, upper_blue)    

        # Bitwise-AND mask and original image  
        img_result = cv2.bitwise_and(frame,frame, mask= mask)  

        cv2.imwrite( 'img_result123.jpg', img_result ) 

        img = cv2.imread('img_result123.jpg')
        img2 = img.copy()
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #Thresholding
        ret, thr = cv2.threshold(imgray, 50, 255, 0)
        _, contours, _ = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for con in contours:
            detect(con)
            
        cv2.imwrite( str(i) +'x'+str( j) +'_detect.jpg', img)

cv2.waitKey(0)
cv2.destroyAllWindows() 



