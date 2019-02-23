import cv2
import numpy as np

cap = cv2.VideoCapture(1)

while(1):

    # Take each frame
    _, frame = cap.read()

    img = frame
    cv2.imshow('frame',frame)
    
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    cv2.imshow("hsv",hsv)
    
    lower_blue=np.array([80,50,50])
    upper_blue=np.array([130,255,255])
    lower_red=np.array([50,50,80])
    upper_red=np.array([255,255,130])
    
    maskB=cv2.inRange(hsv,lower_blue,upper_blue)
    result=cv2.bitwise_and(img,img,mask=maskB)
    
    cv2.imshow('res',result)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    
cv2.destroyAllWindows()