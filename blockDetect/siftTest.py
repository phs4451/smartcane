import numpy as np
import cv2
import sys
from wand.image import Image

detector = cv2.xfeatures2d.SURF_create()

oldfilename = "2.png"
row = 3
col = 3

with Image(filename = oldfilename) as image:

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
                
#cut image

cutimg = [[0 for i in range(row)] for j in range(col)]

goodcount = [[0 for i in range(row)] for j in range(col)] # matched count


for i in range(0, row): 
          for j in range(0, col): 
                cut = cv2.imread(filename="{0}x{1}_{2}".format(i, j, "cutresult.jpg"))
                cutimg[i][j] = cv2.cvtColor(cut,cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(cutimg[i][j],(3,3),0)
                cv2.imwrite("blur.jpg",blur)
                result_edge2 = cv2.Canny(blur, 100, 200)
                cv2.imwrite("edge_result2.png", result_edge2)
                
                #imgRGB2 = cv2.cvtColor(cutimg[i][j], cv2.COLOR_BGR2RGB)
                #result_edge2 = cv2.Canny(imgRGB2, 100, 200)
                #cv2.imwrite("edge_result2.png", result_edge2) 
                
                # edge processing
          
                img3 = cv2.imread('1.jpg')#cv2.imread('target1.jpg')   #cv2.imread('edge_result1.png',0) # template
                img4 = cv2.imread('edge_result2.png') #cutimg[i][j]  #cv2.imread('edge_result2.png')
                
                kp1, des1 = detector.detectAndCompute(img3, None)
                kp2, des2 = detector.detectAndCompute(img4, None)
                
                bf = cv2.BFMatcher()
                matches = bf.knnMatch(des1,des2, k=2)

                good = []
                match_param = 0.7
                for m,n in matches:
                  if m.distance < match_param*n.distance:
                    good.append([m])
                
                img5 = cv2.drawMatchesKnn(img3,kp1,img4,kp2,good, None,flags=2)
                
                print(len(good))
                
                goodcount[i][j] = len(good)

print("\n")

for i in range(0, row): 
          for j in range(0, col): 
              print(goodcount[i][j])
          print("\n")              



#imgRGB2 = cv2.cvtColor(cutimg[2][1], cv2.COLOR_BGR2RGB)
#result_edge2 = cv2.Canny(imgRGB, 100, 200) 
#cv2.imwrite("edge_result2.png", result_edge2)


#img3 = cv2.imread('edge_result1.png',0)
#img4 = cv2.imread('edge_result2.png',0)



#detector = cv2.xfeatures2d.SURF_create()

#kp1, des1 = detector.detectAndCompute(img3, None)
#kp2, des2 = detector.detectAndCompute(img4, None)

#bf = cv2.BFMatcher()
#matches = bf.knnMatch(des1,des2, k=2)

#good = []
#match_param = 0.75
#for m,n in matches:
#  if m.distance < match_param*n.distance:
#    good.append([m])

#img5 = cv2.drawMatchesKnn(img3,kp1,img4,kp2,good, None,flags=2)

#print(len(good))
#cv2.imwrite("shift_result.png", img5)
