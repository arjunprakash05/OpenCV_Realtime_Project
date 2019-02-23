import numpy as np
import cv2
import os,os.path
from numpy import empty
tc=1
f=1
maxOffset=-1
hog = cv2.HOGDescriptor()
hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
dir="VIDEO"+str(tc)
loopFrame=len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))])

while(f<=loopFrame) :
    image = cv2.imread(dir+ "/TC" + str(tc) + "_f1 (" + str(f) + ").jpg")
    image= cv2.flip(image,1)
    height,width,channel=image.shape
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower = (10, 80, 220) #24,68,240
    upper = (38, 126, 255)
    mask = cv2.inRange(hsv, lower, upper)
    mask=mask.copy()[0:height,width/2-250:width/2-50]
    #print hsv[300,550]
    #cv2.circle(hsv,(550,300),4,(255,255,255),-1)
    kernelOpen = np.ones((10,10),np.uint8)
    kernelClose = np.ones((15,15),np.uint8)
    mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernelClose)
    #mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    
#     cnts= cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[1]
#     for c in cnts:
#         # if the contour is too small, ignore it
#         rect = cv2.minAreaRect(c)
#         box = cv2.boxPoints(rect)
#         box = np.int0(box)
#         cv2.drawContours(mask,[box],0,(255,255,255),-1)
#     
    #cv2.imshow("mask",mask)
    canny=cv2.Canny(mask,50,150,apertureSize = 3)
    #cv2.imshow("canny",canny)
    
    lines = cv2.HoughLines(canny,5, np.pi/180, 2, 2,0,0)
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

    if(x1==x2):
        slope=float(float((y1-y2))/float(0.000000001))
    else :
        slope=float(float((y1-y2))/float((x1-x2)))
    #print slope
    
    offset_x_y0=float(float(0-y2)/float(slope)) + x2 + (width/2-250)
    offset_x_yheight=float(float(height-y2)/float(slope)) + x2 + (width/2-250)

    if offset_x_y0>=offset_x_yheight:
        offset_x=offset_x_y0
    else:
        offset_x=offset_x_yheight
    
    if(maxOffset<offset_x):
        maxOffset=offset_x
    roi_platform=image.copy()[0:height,0:maxOffset+50]
    #cv2.imshow("roi_platform",roi_platform)
    found=hog.detectMultiScale(roi_platform, winStride=(8,8), padding=(0,0), scale=1.05)[0]
    col=(0,255,0)
    for x, y, w, h in found:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        bod_x,bod_y,bod_w,bod_h=x+pad_w,y+pad_h,w-3*pad_w,h-3*pad_h
        line_x_old=((bod_y+bod_h)-y2)/slope + x2 + (width/2-250)
        line_x=float(float(((bod_y+bod_h)-y2))/float(slope)) + x2 + (width/2-250)
        cv2.circle(image,(int(line_x_old),bod_y+bod_h),10,(255,0,255),2)
        cv2.circle(image,(int(line_x),bod_y+bod_h),5,(255,255,255),-1)
        if(line_x<=bod_x+bod_w):
            col=(0,0,255)
        cv2.rectangle(image, (bod_x,bod_y), (bod_x+bod_w, bod_y+bod_h), col, 1)
        
    cv2.line(image,(x1+width/2-250,y1),(x2+width/2-250,y2),col,2)

    cv2.imshow("image",image)
    f+=1
    #cv2.waitKey(0)
    k=cv2.waitKey(100) & 0xFF
    if k==27:
        break;

cv2.destroyAllWindows()