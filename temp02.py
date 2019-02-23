import cv2
import numpy as np

img = cv2.imread('real-life-01.jpg',3)
print "Started.."
kernel = np.ones((5,5),np.uint8)
erosion = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel)
erosion = cv2.morphologyEx(erosion,cv2.MORPH_CLOSE,kernel)
erosion = cv2.cvtColor(erosion,cv2.COLOR_BGR2HSV)
print "Starting Loop.."
height=img.shape[0]
width=img.shape[1]
for i in range(0,height-1):
    for j in range(0,width-1):
        if (erosion.item(i,j,0) - erosion.item(i,j+1,0)>10) :
            img.itemset((i,j-1,0),0)
            img.itemset((i,j-1,1),0)
            img.itemset((i,j-1,2),255)
            img.itemset((i,j-2,0),0)
            img.itemset((i,j-2,1),0)
            img.itemset((i,j-2,2),255)
            
            img.itemset((i,j,0),0)
            img.itemset((i,j,1),0)
            img.itemset((i,j,2),255)

        if (erosion.item(i,j,0) - erosion.item(i+1,j,0)>10) :
            img.itemset((i-1,j,0),0)
            img.itemset((i-1,j,1),0)
            img.itemset((i-1,j,2),255)
            img.itemset((i-2,j,0),0)
            img.itemset((i-2,j,1),0)
            img.itemset((i-2,j,2),255)
            
            img.itemset((i,j,0),0)
            img.itemset((i,j,1),0)
            img.itemset((i,j,2),255)

cv2.imwrite("real-life-01-edit.jpg",img)
print "DONE"