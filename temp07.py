import cv2
import numpy as np
from matplotlib import pyplot as plt


cap = cv2.VideoCapture(1)

while(1):

    # Take each frame
    _, img = cap.read()
    
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    height,width=gray.shape
    img1=img.copy()
    img2=img.copy()
    img3=img.copy()
    # global thresholding
    ret1,th1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    
    # Otsu's thresholding
    ret2,th2 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    # Otsu's thresholding after Gaussian filtering
    blur = cv2.GaussianBlur(gray,(5,5),0)
    ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    # plot all the images and their histograms
    images = [img, 0, th1,
              img, 0, th2,
              blur, 0, th3]
    titles = ['Original Noisy Image','Histogram','Global Thresholding (v=127)',
              'Original Noisy Image','Histogram',"Otsu's Thresholding",
              'Gaussian filtered Image','Histogram',"Otsu's Thresholding"]
    
#     th1=cv2.bitwise_not(th1)
#     th2=cv2.bitwise_not(th2)
#     th3=cv2.bitwise_not(th3)
    
    cv2.imshow("th2",th2)
    
    _,contours1,hierarchy1= cv2.findContours(th1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    _,contours2,hierarchy2= cv2.findContours(th2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    _,contours3,hierarchy3= cv2.findContours(th3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    count=0
    for contour in contours1 :
        rect=cv2.boundingRect(contour)
        if ( rect[2] < width/10 or rect[3] < height/10 ) or ( rect[2]>width/2 or rect[3]>height/2):
            continue
        x,y,w,h = rect
        cv2.rectangle(img1,(x,y),(x+w,y+h),(0,255,0),2)
        objcount="Object #" + str(count+1)
        cv2.putText(img1,objcount,(x+10,y),0,1.3,(0,255,0))
        count=count+1
    cv2.imshow('frame1',img1)
    
    count=0
    for contour in contours1 :
        rect=cv2.boundingRect(contour)
        if ( rect[2] < width/10 or rect[3] < height/10 ) or ( rect[2]>width/2 or rect[3]>height/2):
            continue
        x,y,w,h = rect
        cv2.rectangle(img2,(x,y),(x+w,y+h),(0,255,0),2)
        objcount="Object #" + str(count+1)
        cv2.putText(img2,objcount,(x+10,y),0,1.3,(0,255,0))
        count=count+1
    cv2.imshow('frame2',img2)    
    
    count=0
    for contour in contours3 :
        rect=cv2.boundingRect(contour)
        if ( rect[2] < width/15 or rect[3] < height/15 ) or ( rect[2]>width/1.5 or rect[3]>height/1.5):
            continue
        x,y,w,h = rect
        cv2.rectangle(img3,(x,y),(x+w,y+h),(0,255,0),2)
        objcount="Object #" + str(count+1)
        cv2.putText(img3,objcount,(x+10,y),0,1.3,(0,255,0))
        count=count+1
    cv2.imshow('frame3',img3)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    
cv2.destroyAllWindows()