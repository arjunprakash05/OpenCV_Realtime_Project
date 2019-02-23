import cv2
import numpy as np

filename="real-life-01.jpg"
img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
height,width = gray.shape
# print height,width
# for i in range(0,height-1):
#     for j in range(0,width-1):
#         if gray.item(i,j)<70:
#             gray.itemset(i,j,0)
#         else :
#             gray.itemset(i,j,255)
#gray=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,115,1)
gray=cv2.inRange(gray,0,50)
cv2.imwrite("minor-" + filename,gray)

# for i in range(0,height-1):
#     for j in range(0,width-1):
#         if gray.item(i,j)==0:
#             if markingLeft==False:
#                 markingLeft=True
#             else :
#                 for k in range(j,width-1):

_,contours,hierarchy= cv2.findContours(gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#cv2.drawContours(img,contours,-1,(0,255,0),5)

cv2.imwrite("minor-contour-" + filename,img)
for contour in contours :
    #print cv2.contourArea(contour)
    rect=cv2.boundingRect(contour)
    if rect[2] < 100 or rect[3] < 100: continue
    print cv2.contourArea(contour)
    x,y,w,h = rect
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        

cv2.imwrite("minor-color-" + filename,img)
print "Finished."
k = cv2.waitKey(0)
cv2.destroyAllWindows()

# cap = cv2.VideoCapture(1)
# fgbg = cv2.createBackgroundSubtractorMOG2()
#  
#  
# while True :
#     ret,frame=cap.read()
#     fgmask=fgbg.apply(frame)
#      
#     cv2.imshow('original',frame)
#     cv2.imshow('fg',fgmask)
#      
#     k=cv2.waitKey(30) & 0xff
#     if k==27 :
#         break
#      
#      
# cap.release()
# cv2.destroyAllWindows()