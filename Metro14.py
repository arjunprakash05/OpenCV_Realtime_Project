import numpy as np
import cv2
import os,os.path
from numpy import empty
tc=14
f=1
dir="VIDEO"+str(tc)
loopFrame=len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))])
fgbg=cv2.createBackgroundSubtractorMOG2()
while(f<=loopFrame) :
    image = cv2.imread(dir+ "/TC" + str(tc) + "_f1 (" + str(f) + ").jpg")
    print f,"/",loopFrame
    image=cv2.resize(image,(854,480))
    height,width,channel=image.shape
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower = (20, 110, 220) #24,68,240
    upper = (35, 145, 255)
    #print hsv[400,247]
    #cv2.circle(hsv,(247,400),4,(255,255,255),-1)
    #cv2.imshow("hsv",hsv)
    mask = cv2.inRange(hsv, lower, upper)
    mask=mask.copy()[0:height,width/2-280:width/2-80]
    kernelOpen = np.ones((5,5),np.uint8)
    kernelClose = np.ones((15,15),np.uint8)
    mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernelClose)
    #mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    #cv2.imshow("mask",mask)
    #cv2.waitKey(0)
#     cnts= cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[1]
#     for c in cnts:
#         # if the contour is too small, ignore it
#         rect = cv2.minAreaRect(c)
#         box = cv2.boxPoints(rect)
#         box = np.int0(box)
#         cv2.drawContours(mask,[box],0,(255,255,255),-1)
#     
    canny=cv2.Canny(mask,50,150,apertureSize = 3)
    #cv2.imshow("canny",canny)
    #cv2.imshow("mask",mask)
    lines = cv2.HoughLines(canny,1, np.pi/180, 10, 2,0,0)
    #print lines.type
    for rho,theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        cv2.line(image,(x1+width/2-280,y1),(x2+width/2-280,y2),(0,0,255),2)


    cv2.imshow("image",image)
    f+=1
    k=cv2.waitKey(1) & 0xFF
    if k==27:
        break;
cv2.waitKey(0)
cv2.destroyAllWindows()