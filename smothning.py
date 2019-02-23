import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('2.jpg')

kernel = np.ones((5,5),np.float32)/25
dst = cv2.filter2D(img,-1,kernel)
blur = cv2.blur(img,(5,5))
blur2 = cv2.GaussianBlur(img,(5,5),0)
median = cv2.medianBlur(img,5)
blur3 = cv2.bilateralFilter(img,9,75,75)
#cv2.imshow('filter',dst)
#cv2.imshow('blur',blur)
#cv2.imshow('Gaussian blur',blur2)
#cv2.imshow('median',median)
#cv2.imshow('BIlateral',blur3)
titles = ['filter','Blur','Gaussian','medianBlur','Bilateral']
images = [dst,blur,blur2,median,blur3]
for i in xrange(5):
    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()