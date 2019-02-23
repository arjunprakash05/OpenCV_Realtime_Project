import cv2
import numpy as np

img=cv2.imread("real-life-01.jpg")
img1=cv2.imread("python-logo.png")
gray=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)

rows,cols,channel=img1.shape
roi=img[0:rows,0:cols]

cv2.imshow("original",img1)

ret,mask=cv2.threshold(gray,220,255,cv2.THRESH_BINARY_INV)
mask_inv=cv2.bitwise_not(mask)

img_bg=cv2.bitwise_and(roi,roi,mask=mask_inv)
img1_fg=cv2.bitwise_and(img1,img1,mask=mask)
img_sum=img_bg+img1_fg

img[0:rows,0:cols]=img_sum

cv2.imshow("res",img)
cv2.imwrite("real-life-01-logo.jpg",img)
cv2.waitKey(0)
cv2.destroyAllWindows()