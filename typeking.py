from PIL import ImageGrab
from PIL import Image
import pytesseract
import numpy as np
import cv2
import matplotlib.pyplot as plt
from sqlalchemy.sql.expression import except_all

def find_image(im, tpl):
    im = np.atleast_3d(im)
    tpl = np.atleast_3d(tpl)
    H, W, D = im.shape[:3]
    h, w = tpl.shape[:2]

    # Integral image and template sum per channel
    sat = im.cumsum(1).cumsum(0)
    tplsum = np.array([tpl[:, :, i].sum() for i in range(D)])

    # Calculate lookup table for all the possible windows
    iA, iB, iC, iD = sat[:-h, :-w], sat[:-h, w:], sat[h:, :-w], sat[h:, w:] 
    lookup = iD - iB - iC + iA
    # Possible matches
    possible_match = np.where(np.logical_and(*[lookup[..., i] == tplsum[i] for i in range(D)]))

    # Find exact match
    for y, x in zip(*possible_match):
        if np.all(im[y+1:y+h+1, x+1:x+w+1] == tpl):
            return (y+1, x+1)

    return (-1,-1)

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
dir="VIDEOTR"
f=1
lower=[150,160,0]
upper=[240,210,5]
lower = np.array(lower, dtype = "uint8")
upper = np.array(upper, dtype = "uint8")
orb = cv2.ORB_create()
while(True):
    img = ImageGrab.grab() #bbox specifies specific region (bbox= x,y,width,height)
    image = np.array(img)
    #frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask = mask)
    output = cv2.cvtColor(output,cv2.COLOR_BGR2GRAY)
    ret, output = cv2.threshold(output, 100 , 255, cv2.THRESH_BINARY)
    
    kernelClose = np.ones((15,15),np.uint8)
    mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernelClose)
    #mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3 , 3)) 
    output = cv2.dilate(mask,kernel,iterations = 9)
    
    #cv2.imshow("test", output)
    
    contours= cv2.findContours(output.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[1]
    for contour in contours :
        #print cv2.contourArea(contour)
        rect=cv2.boundingRect(contour)
        if rect[3] < 25 : continue
        #print cv2.contourArea(contour)
        x,y,w,h = rect
        #cv2.rectangle(image,(x+5,y+5),(x+w-5,y+h-5),(0,255,0),2)
        cropped = image[y + 5 : y +  h - 5 , x + 5 : x + w - 5]
        cropped= cv2.resize(cropped,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)

        d="Output/"+dir+"/Img(" + str(f) + ").jpg"
        
        i=cv2.imread("Output/"+dir+"/TrainData/105.jpg")
        
        y,x = find_image(cropped,i)
        if not (x == -1 and y == -1) :
            d="Output/"+dir+"/Img(" + str(f) + ")_i.jpg"
            print 'i found'
        else :
            d="Output/"+dir+"/Img(" + str(f) + ")_no_i.jpg"
            print 'not found'
        
        #img3= cv2.drawMatches(i,kp1,cropped,kp2,matches,None,flags=2)
        #plt.imshow(img3)
        #plt.show()
        
        cv2.imwrite(d,cropped)
        #cv2.imshow("test", cropped)
        #cv2.imwrite(d,cropped)
        #print pytesseract.image_to_string(Image.open(d),lang='eng')
        f=f+1
        break
    
    #print image_to_string(Image.open("Output/"+dir+"/Img (" + str(f) + ").jpg)", lang='eng')
    
    k=cv2.waitKey(50) & 0xFF
    if k==27:
        break;
#cv2.waitKey(0)
cv2.destroyAllWindows()