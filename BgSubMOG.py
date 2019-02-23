import numpy as np
import cv2
from cmath import rect

cap = cv2.VideoCapture(0)

fgbg = cv2.createBackgroundSubtractorMOG2() 

while(1):
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)
    _,contours,hierarchy = cv2.findContours(fgmask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours :
        rect=cv2.boundingRect(contour)
        if rect[2]<100 or rect[3]<100 :
            continue  
        x,y,w,h = rect
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imshow('frame',frame)
    cv2.imshow('mask',fgmask)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()