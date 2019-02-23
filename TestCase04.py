import numpy as np
import cv2
import os,os.path
tc=1
f=1
dir="VIDEO"+str(tc)
loopFrame=len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))])

while(f<=loopFrame) :
    image = cv2.imread(dir+ "/TC" + str(tc) + "_f1 (" + str(f) + ").jpg")
    height,width,channel=image.shape
    image=cv2.GaussianBlur(image,(15,15),0)
    lower = (85, 175, 205)
    upper = (145, 245, 255)
    mask = cv2.inRange(image, lower, upper)
    
    kernelOpen = np.ones((10,10),np.uint8)
    kernelClose = np.ones((15,15),np.uint8)
    mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernelClose)
    mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    
    cv2.imshow("mask",mask)
    canny=cv2.Canny(mask,50,150,apertureSize = 3)
    cv2.imshow("canny",canny)
    
    lines = cv2.HoughLines(canny,1, np.pi/2, 6, None, 50, 10)
    for rho,theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
  
        cv2.line(image,(x1,y1),(x2,y2),(0,0,255),2)
    
    
    
    cv2.imshow("image",image)
    f+=1
    cv2.waitKey(0)
    k=cv2.waitKey(100) & 0xFF
    if k==27:
        break;

cv2.destroyAllWindows()