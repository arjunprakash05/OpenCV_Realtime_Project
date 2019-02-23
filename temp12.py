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

cv2.imshow("Background",bgref)
while(1):

    # Take each frame
    _, img = cap.read()
    
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    
    frameDelta = cv2.absdiff(bgref, gray)
    thresh = cv2.threshold(frameDelta, 10, 255, cv2.THRESH_BINARY)[1]
 
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=1)
    cv2.imshow("thresh",thresh)
    cnts= cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[1]
 
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
    
    k = cv2.waitKey(25) & 0xFF
    if k == 27:
        break
    
cap.release()
cv2.destroyAllWindows()