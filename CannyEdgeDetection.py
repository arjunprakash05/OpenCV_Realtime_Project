import cv2
import numpy as np
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)
kernal=np.ones((5,5),np.uint8)
while True :
    ret,frame_cur=cap.read()
    frame_cur = cv2.cvtColor(frame_cur,cv2.COLOR_BGR2GRAY)
    closing = cv2.morphologyEx(frame_cur,cv2.MORPH_CLOSE,kernal)
    
    closing = cv2.threshold(closing,127,255,cv2.THRESH_BINARY)
    
    
    cv2.imshow("closig-before",closing)
    _,contours,hierarchy = cv2.findContours(closing,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours :
        rect=cv2.boundingRect(contour)
        if rect[2]<30 or rect[3]<30 :
            continue  
        x,y,w,h = rect
        cv2.rectangle(frame_cur,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imshow('frame',frame_cur)
    cv2.imshow('mask',closing)
    #cv2.imshow('pre',thresh)
    #cv2.imshow('cur',thresh_cur)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()