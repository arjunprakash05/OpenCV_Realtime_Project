import numpy as np
import cv2
import os,os.path
tc=1
f=1
dir="VIDEO"+str(tc)
loopFrame=len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))])

while(f<=loopFrame) :
    image = cv2.imread(dir+ "/TC" + str(tc) + "_f1 (" + str(f) + ").jpg")
    lower = (85, 175, 205)
    upper = (145, 245, 255)
    height,width,channel=image.shape
    mask = cv2.inRange(image, lower, upper)
    cv2.imshow("inRange",mask)
    kernelOpen = np.ones((3,3),np.uint8)
    kernelClose = np.ones((10,10),np.uint8)
    erosion = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernelClose)
    erosion = cv2.morphologyEx(erosion,cv2.MORPH_OPEN,kernelOpen)
    cv2.imshow("dilate",erosion)
    roi=erosion[0:height,width/3-100:2*width/3+100]
    #cv2.imshow("Dd",roi)
    #output = cv2.bitwise_and(image, image, mask = roi)
    #cv2.imshow("output",output)
    cnts= cv2.findContours(roi.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[1]
    # loop over the contours
    maxHeight=-1
    for c in cnts:
        # if the contour is too small, ignore it
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        box[0][0]+=width/3-100
        box[1][0]+=width/3-100
        box[2][0]+=width/3-100
        box[3][0]+=width/3-100
        cv2.drawContours(image,[box],0,(0,0,255),2)
        #cv2.line(image,(box[1][0],box[1][1]),(box[2][0],box[2][1]),(0,0,255),4)
#         ellipse = cv2.fitEllipse(c)
#         im = cv2.ellipse(image,ellipse,(0,255,0),2)

#         (x, y, w, h) = cv2.boundingRect(c)
#         if h<height/5:
#             continue
# 
#         cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         rect = cv2.minAreaRect(c)
#         box = cv2.boxPoints(rect)
#         box = np.int0(box)
        cv2.imshow("images",image)
        cv2.waitKey(0)
        
    f+=1
    k=cv2.waitKey(100) & 0xFF
    if k==27:
        break;

cv2.destroyAllWindows()