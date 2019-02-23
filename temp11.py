import cv2
import numpy as np
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(1)
i=0
frames=[]
#cv2.imshow("Background",bgref)
while(i<10):

    # Take each frame
    _, img = cap.read()
    
    cv2.imshow("img",img)
    frames.append(img)
    k = cv2.waitKey(2000)
    
    i=i+1
    
cap.release()
    
cv2.destroyAllWindows()