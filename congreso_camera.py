import cv2
# from skimage.metrics import structural_similarity as ss
from matplotlib import pyplot as plt

vid=cv2.VideoCapture(1)

def show(image):
    # image=cv2.resize(image,(900,900))
    cv2.imshow('imagen',image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
try:
    while True:
        result=False
        a=10
        #sigue tomando foto hasta que salga un resultado positivo
        while not(result) and a>=0:
            result,image=vid.read()
            a-=1


        im1=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

        #blur image 
        im1=cv2.blur(im1,(5,5))
        #set threshold
        _,t=cv2.threshold(im1,100,255,cv2.THRESH_BINARY_INV)
        c,b=cv2.findContours(t,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        im1=cv2.drawContours(image,c,-1,(0,255,0),1)
        show(im1)

except KeyboardInterrupt:
    vid.release()