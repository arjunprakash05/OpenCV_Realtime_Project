import cv2
import numpy as np
from matplotlib import pyplot as plt


cap = cv2.VideoCapture(1)
i=0
while(i<10):
    _, img = cap.read()
    i=i+1
    k = cv2.waitKey(25)

bgref=img.copy()
bgref=cv2.cvtColor(bgref,cv2.COLOR_BGR2GRAY)

thresh_bg= cv2.inRange(bgref,127,255)

cv2.imshow("Background",bgref)
while(1):

    # Take each frame
    _, img = cap.read()
    bg=img.copy()
    
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    h,w=gray.shape
    
    diff1= cv2.subtract(bgref,gray)
    diff2= cv2.subtract(gray,bgref)
    diff=cv2.bitwise_or(diff1,diff2)
    #print diff.item(0,0,0),gray.item(0,0,0)
    #diff.item(40,40,1),diff.item(40,40,2)
    diff=cv2.inRange(diff,50,255)

#     for i in range(0,h-1):
#         for j in range(0,w-1):
#             if gray.item(i,j)-bgref.item(i,j)>5 or gray.item(i,j)-bgref.item(i,j)<-5 :
#               `  diff.itemset(i,j,255)
#             else:
#                 diff.itemset(i,j,0) 

    _,contours,hierarchy= cv2.findContours(diff.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
     
    count=0
    for contour in contours :
        rect=cv2.boundingRect(contour)
        if rect[2] < 100 or rect[3] < 100 :
            continue
        x,y,w,h = rect
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        objcount="Object #" + str(count+1)
        cv2.putText(img,objcount,(x+10,y+h-10),0,0.5,(0,255,0))
        count=count+1
    cv2.imshow('frame',img)
    
    cv2.imshow("balha",gray)
    cv2.imshow("diff",diff)
    if(i%20==0):
        bgref=cv2.cvtColor(bg,cv2.COLOR_BGR2GRAY)
        i=0
    i=i+1
    k = cv2.waitKey(25) & 0xFF
    if k == 27:
        break
    
cv2.destroyAllWindows()