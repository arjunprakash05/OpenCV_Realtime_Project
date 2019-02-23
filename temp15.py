import numpy as np
import cv2

image = cv2.imread("testcases/img03.jpg")
lower = (120, 140, 160)
upper = (150, 170, 190)
height,width,channel=image.shape
mask = cv2.inRange(image, lower, upper)
mask = cv2.dilate(mask,None,iterations=1)
output = cv2.bitwise_and(image, image, mask = mask)
cnts= cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[1]

# loop over the contours
for c in cnts:
    #if the contour is too small, ignore it
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(image,[box],0,(0,0,255),2)
    (x, y, w, h) = cv2.boundingRect(c)
    #if h<height/5:# or w>width/100:
    #    continue

    # compute the bounding box for the contour, draw it on the frame,
    # and update the text
    #cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow("images",image)
cv2.waitKey(0)