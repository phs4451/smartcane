
import cv2

img1 = cv2.imread('test1.jpg')
img2= cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(img2,(3,3),0)
result_edge2 = cv2.Canny(blur, 100, 200)
cv2.imwrite("edge.png", result_edge2)

