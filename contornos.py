import cv2
# from skimage.metrics import structural_similarity as ss
from matplotlib import pyplot as plt
import numpy as np
import time

vid=cv2.VideoCapture(1)

def show(image):
    # image=cv2.resize(image,(900,900))
    cv2.imshow('imagen',image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return

try:
    # while True:
    for y in range(5):
        result=False
        a=10
        #keeps taking photos until obtaining a positive result
        while not(result) and a>=0:
            result,image=vid.read()
            a-=1

        im1=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

        #blur image 
        im1=cv2.blur(im1,(5,5))
        #set threshold
        _,t=cv2.threshold(im1,100,255,cv2.THRESH_BINARY_INV)#threshold value (100 in this code) should be variable to adjust itself depending the image
        c,b=cv2.findContours(t,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        time.sleep(10)
        print("foto: ",y+1)
    center=np.array([image.shape[1]//2,image.shape[0]//2]) #image center (x,y)
    # mini=np.array([image.shape[1],image.shape[0]]) #image size (x,y)
    image=cv2.circle(image,center,1,(255,0,0),10)
    for w in range(len(c)):
        if len(c[w])>300 and len(c[w])<1500:
            midp=c[w][len(c[w])//2]
            print("punto medio: ",midp)#midpoint of contour
            image=cv2.circle(image,midp[0],1,(255,255,0),100)
            im1=cv2.drawContours(image,c,w,(0,255,0),1)
            # for v in c[w]: #looking for the closes point to center
            #     print("point: ",v,end='')
            print('distancia: ',np.subtract(center,midp))
            print('showing contour: ',w)            
            print(image.shape[1]//2,image.shape[0]//2)
            show(im1)
        else:
            continue
    
except KeyboardInterrupt:
    vid.release()

else:
    vid.release()