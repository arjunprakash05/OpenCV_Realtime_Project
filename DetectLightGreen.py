import cv2
import numpy as np

img = cv2.VideoCapture(0)

ORANGE_MIN = np.array([63, 125, 114],np.uint8)
ORANGE_MAX = np.array([103, 165, 154],np.uint8)

while True:
    ret,frame =img.read()
    hsv_img = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    kernal=np.ones((5,5),np.uint8)/25
    frame_threshed = cv2.inRange(hsv_img, ORANGE_MIN, ORANGE_MAX)
    dilation = cv2.dilate(frame_threshed,kernal,iterations=1)
    _,contours,hierarchy = cv2.findContours(dilation.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours :
        rect=cv2.boundingRect(contour)
        if rect[2]<30 or rect[3]<30 :
            continue  
        x,y,w,h = rect
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imshow('frame',frame)
    cv2.imshow('mask',frame_threshed)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

img.release()
cv2.destroyAllWindows()