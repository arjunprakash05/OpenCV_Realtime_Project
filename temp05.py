import cv2
import numpy as np

cap = cv2.VideoCapture(1)

while(1):

    # Take each frame
    _, frame = cap.read()

    img = frame
    
    gray1=gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    height,width = gray.shape
    cv2.imwrite("minor-gray-real-life-01.jpg",gray)
    
    ##THRESHHOLDING
    gray=cv2.inRange(gray,0,50)
    #gray=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,115,1)
    
    cv2.imshow('gray',gray)
    _,contours,hierarchy= cv2.findContours(gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    #cv2.drawContours(img,contours,-1,(0,255,0),5)

    for contour in contours :
    #print cv2.contourArea(contour)
        rect=cv2.boundingRect(contour)
        if rect[2] < 80 or rect[3] < 80:
            continue
        x,y,w,h = rect
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    
    cv2.imshow('frame',img)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    
cv2.destroyAllWindows()