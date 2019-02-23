import cv2
import numpy as np

cap = cv2.VideoCapture(1)

while(1):

    # Take each frame
    _, frame = cap.read()
    cv2.imshow("frameorig",frame)
    img = frame
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    height,width = gray.shape
    
    ##THRESHHOLDING
    #gray=cv2.inRange(gray,0,50)
    #cv2.imshow('gray-original',gray)
    gray=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,5)
    
    ##MORPHOLOGY
    kernel = np.ones((15,15),np.int8)/225
    #gray= cv2.morphologyEx(gray,cv2.MORPH_OPEN,kernel)
    gray = cv2.morphologyEx(gray,cv2.MORPH_CLOSE,kernel)
    #gray=cv2.erode(gray,kernel,iterations=1)
    #gray = cv2.dilate(gray,kernel,iterations = 1)
    
    #NOISE REDUCTION
    #gray=cv2.GaussianBlur(gray,(15,15),0)
    
    #BLUR EFFECTS
    #gray = cv2.medianBlur(gray,25)
    
    cv2.imshow('gray-processed',gray)
    _,contours,hierarchy= cv2.findContours(gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    #cv2.drawContours(img,contours,-1,(0,255,0),5)
    count=0
    for contour in contours :
    #print cv2.contourArea(contour)
        rect=cv2.boundingRect(contour)
        if rect[2] < 100 or rect[3] < 100:
            continue
        x,y,w,h = rect
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        objcount="Object #" + str(count+1)
        cv2.putText(img,objcount,(x+10,y),0,1.3,(0,255,0))
        count=count+1
    cv2.imshow('frame',img)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    
cv2.destroyAllWindows()