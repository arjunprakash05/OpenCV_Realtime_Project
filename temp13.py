import cv2
import numpy as np
import time
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(1)
time.sleep(0.25)
_, img = cap.read()

bgref =img.copy()
bgref =cv2.cvtColor(bgref,cv2.COLOR_BGR2GRAY)
bgref = cv2.GaussianBlur(bgref, (21, 21), 0)
oldbg=bgref.copy()
i=0
kernel=np.ones((3,3),np.uint8)
while(1):

    # Take each frame
    _, img = cap.read()
    
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    bg=gray.copy()
#     frameDelta = cv2.absdiff(bgref, oldbg)
#     thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY_INV)[1]
#     thresh = cv2.dilate(thresh, None, iterations=1)
#     frameDelta=cv2.bitwise_and(bgref,oldbg,mask=thresh)
#     
    frameDelta = cv2.absdiff(bgref, gray)
    thresh = cv2.threshold(frameDelta, 5, 255, cv2.THRESH_BINARY)[1]
 
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    #thresh = cv2.dilate(thresh, None, iterations=1)
    ghost=thresh.copy()
    mask=cv2.absdiff(bgref,oldbg)
    mask = cv2.threshold(mask, 5, 255, cv2.THRESH_BINARY_INV)[1]
    mask= cv2.erode(mask, kernel, iterations=1)
    ghost=cv2.bitwise_and(thresh,thresh,mask=mask)
    ghost=cv2.dilate(ghost,None,iterations=1)
    cv2.imshow("ghost",ghost)
    cnts= cv2.findContours(ghost.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[1]
    
    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        (x, y, w, h) = cv2.boundingRect(c)
        if w<100 or h<100:
            continue
 
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    cv2.imshow("obj",img)
    if(i%40==0):
        bgref=bg.copy()
        i=0
    i=i+1
    k = cv2.waitKey(25) & 0xFF
    if k == 27:
        break
    
cap.release()
cv2.destroyAllWindows()