import numpy as np
import cv2

body_cascade=cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
cap=cv2.VideoCapture(1)

while True :
    
    ret,image=cap.read()
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    bodies=body_cascade.detectMultiScale(gray,2,5)
    
    for (x,y,w,h) in bodies :
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
    
    cv2.imshow("image",image)
    k=cv2.waitKey(25) & 0xFF
    if k==27:
        break;
cap.release()    
cv2.destroyAllWindows()