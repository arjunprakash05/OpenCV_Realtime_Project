import numpy as np
import cv2
import os,os.path
from numpy import empty
tc=17
f=1
dir="VIDEO"+str(tc)
loopFrame=len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))])
maxOffset=-1
hog = cv2.HOGDescriptor()
hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

while(f<=loopFrame) :
    image= cv2.imread(dir+ "/TC" + str(tc) + "_f1 (" + str(f) + ").jpg")
    print f,"/",loopFrame
    image=cv2.resize(image,(1080/3,1920/3))
    height,width,channel=image.shape
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    hsv=cv2.blur(hsv,(5,5))
    lower = (0, 100, 200) #24,68,240
    upper = (50, 205, 255)
    #print hsv[550,185]
    #cv2.circle(hsv,(185,550),4,(255,255,255),-1)
    #cv2.imshow("hsv",hsv)
    mask = cv2.inRange(hsv, lower, upper)
    mask=mask.copy()[0:height,width/2-50:width/2+50]
    kernelOpen = np.ones((5,5),np.uint8)
    kernelClose = np.ones((15,15),np.uint8)
    mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernelClose)
    mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
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
    #canny= cv2.morphologyEx(canny,cv2.MORPH_OPEN,kernelOpen)
    #cv2.imshow("canny",canny)
    #cv2.imshow("mask",mask)
    lines = cv2.HoughLines(canny,2, np.pi/150, 10, 2,0,0)
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
    
    offset_x_y0=float(float(0-y2)/float(slope)) + x2 + (width/2-50)
    offset_x_yheight=float(float(height-y2)/float(slope)) + x2 + (width/2-50)

    if offset_x_y0>=offset_x_yheight:
        offset_x=offset_x_y0
    else:
        offset_x=offset_x_yheight
    
    if(maxOffset<offset_x):
        maxOffset=offset_x
    roi_platform=image.copy()[0:height,0:maxOffset+50]
    
    found=hog.detectMultiScale(roi_platform, winStride=(6,6), padding=(0,0), scale=1.05)[0]
    col=(0,255,0)
    for x, y, w, h in found:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        bod_x,bod_y,bod_w,bod_h=x+pad_w,y+pad_h,w-3*pad_w,h-3*pad_h
        line_x_old=((bod_y+bod_h)-y2)/slope + x2 + (width/2-50)
        line_x=float(float(((bod_y+bod_h)-y2))/float(slope)) + x2 + (width/2-50)
        cv2.circle(image,(int(line_x_old),bod_y+bod_h),10,(255,0,255),2)
        cv2.circle(image,(int(line_x),bod_y+bod_h),5,(255,255,255),-1)
        if(line_x<=bod_x+bod_w):
            col=(0,0,255)
        cv2.rectangle(image, (bod_x,bod_y), (bod_x+bod_w, bod_y+bod_h), col, 1)
        
    
        
    cv2.line(image,(x1+width/2-50,y1),(x2+width/2-50,y2),col,2)
    
    cv2.imshow("image",image)
    #cv2.imwrite("Output/"+dir+"/TC" + str(tc) + "_f1 (" + str(f) + ").jpg",image)
    f+=1
    k=cv2.waitKey(1) & 0xFF
    if k==27:
        break;
cv2.waitKey(0)
cv2.destroyAllWindows()