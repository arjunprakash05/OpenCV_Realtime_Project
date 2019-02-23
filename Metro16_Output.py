import numpy as np
import cv2
import os,os.path
from numpy import empty
tc=16
f=1
dir="Output/VIDEO"+str(tc)
loopFrame=len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))])

while(f<=loopFrame) :
    image= cv2.imread(dir+ "/TC" + str(tc) + "_f1 (" + str(f) + ").jpg")
    print f,"/",loopFrame
    cv2.imshow("image",image)
    f+=1
    k=cv2.waitKey(1) & 0xFF
    if k==27:
        break;
cv2.waitKey(0)
cv2.destroyAllWindows()