from collections import deque
import numpy as np
import cv2
 
# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
cap = cv2.VideoCapture(1)
i=0
while(i<10):
    _, img = cap.read()
    i=i+1
    k = cv2.waitKey(25)

bgref=img.copy()
bgref=cv2.cvtColor(bgref,cv2.COLOR_BGR2GRAY)
kernel=np.ones((15,15), np.uint8)/225
bgref=cv2.dilate(bgref,kernel,iterations=1)
thresh_bg= cv2.inRange(bgref,127,255)

cv2.imshow("Background",bgref)
pts = deque(maxlen=10)
while True:
    # grab the current frame
    _, img = cap.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    h,w=gray.shape
    gray=cv2.erode(gray,kernel,iterations=1)
    diff= cv2.absdiff(bgref,gray)
    #print diff.item(0,0,0),gray.item(0,0,0)
    #diff.item(40,40,1),diff.item(40,40,2)
    diff=cv2.inRange(diff,50,255)

    mask = cv2.erode(diff, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cv2.imshow("jj",mask)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
 
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # only proceed if the radius meets a minimum size
        if radius > 10:
        # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(img, (int(x), int(y)), int(radius),(0, 255, 255), 2)
            cv2.circle(img, center, 5, (0, 0, 255), -1)
 
    # update the points queue
    pts.appendleft(center)

    for i in xrange(1, len(pts)):
    # if either of the tracked points are None, ignore
    # them
        if pts[i - 1] is None or pts[i] is None:
            continue
 
    # otherwise, compute the thickness of the line and
    # draw the connecting lines
        thickness = int(np.sqrt(10/ float(i + 1)) * 2.5)
        cv2.line(img, pts[i - 1], pts[i], (0, 0, 255), thickness)
 
    # show the frame to our screen
    cv2.imshow("Frame", img)
    key = cv2.waitKey(1) & 0xFF
 
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
 
# cleanup the camera and close any open windows
cap.release()
cv2.destroyAllWindows()