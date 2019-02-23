import cv2
import numpy as np

cap = cv2.VideoCapture(1)

while(1):

    # Take each frame
    _, frame = cap.read()

    img = frame
    cv2.imshow('frame',frame)
    
    kernel = np.ones((5,5),np.uint8)
    noiseless = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel)

    noiseless = cv2.morphologyEx(noiseless,cv2.MORPH_CLOSE,kernel)

    noiseless=cv2.cvtColor(noiseless,cv2.COLOR_BGR2HSV)

    height=img.shape[0]
    width=img.shape[1]
    for i in range(0,height-1):
        for j in range(0,width-1):
            if (noiseless.item(i,j,0) - noiseless.item(i,j+1,0) >15) or (noiseless.item(i,j,0) - noiseless.item(i,j+1,0) < -15) :
                img.itemset((i,j,0),0)
                img.itemset((i,j,1),0)
                img.itemset((i,j,2),255)

            if (noiseless.item(i,j,0) - noiseless.item(i+1,j,0) >15) or (noiseless.item(i,j,0) - noiseless.item(i+1,j,0) < -15) :
                img.itemset((i,j,0),0)
                img.itemset((i,j,1),0)
                img.itemset((i,j,2),255)
    
    cv2.imshow('hsv',noiseless)
    cv2.imshow('res',img)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    
cv2.destroyAllWindows()