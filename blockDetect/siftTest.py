import numpy as np
import cv2
img1 = cv2.imread('target.jpg',0)
img2 = cv2.imread('testno.jpg',0)

detector = cv2.xfeatures2d.SURF_create()

kp1, des1 = detector.detectAndCompute(img1, None)
kp2, des2 = detector.detectAndCompute(img2, None)

bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2, k=2)

good = []
match_param = 0.9
for m,n in matches:
  if m.distance < match_param*n.distance:
    good.append([m])

img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good, None,flags=2)
cv2.imwrite("shift_result.png", img3)