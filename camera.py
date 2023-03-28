##gets image from a camera and displays it on the screen

# import the opencv library
import cv2
import numpy as np
from scipy.spatial import distance

def camera(image=''):
    if image=='':
        # define a video capture object
        vid = cv2.VideoCapture(0)

        #read image
        result=False
        a=0
        while not(result) and a<=10:
            result, image = vid.read()
            a+=1
        vid.release()
        if not(result):
            return 'no image'
    else:
        image=cv2.imread(image)
    #get contour on image
    im1=cv2.medianBlur(image,5)

    im1=cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)

    #getting threshold
    _,t=cv2.threshold(im1,100,255,cv2.THRESH_BINARY_INV)

    c,b=cv2.findContours(t,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    im1=cv2.drawContours(im1,c,-1,(0,255,0),1)
    
    #set image center
    center=np.flip(np.floor_divide(image.shape[0:2],2))
    image=cv2.circle(image,center,2,(255,0,0),3)

    circles=cv2.HoughCircles(im1,cv2.HOUGH_GRADIENT,1,40,
                             param1=150,param2=20,
                             minRadius=7,maxRadius=30)
    
    try:
        circles=np.uint16(np.around(circles))
        
        #encontrar ecuacion para distancia entre puntos
        cls=0
        for i in circles[0,:]:
            dst=distance.euclidean(i[:2],center)
            if cls==0 or dst<cls:
                cls=dst
                x=i
        cv2.circle(image,(x[0],x[1]),x[2],(0,255,0),2) #borde del tornillo
        cv2.circle(image,(x[0],x[1]),2,(0,0,255),3) #centro del tornillo
        z=(np.subtract(np.flip(center),x[0:2])) #diferencia entre el centro y el tornillo mas cercano
        return z
        # print(z)
        # print(x)
        # print(center)
        
    except IndexError:
        return 'no screw detected'
        # print('no screw found')

    
    #display image
    cv2.imshow('prueba',image)

    #0, press any key to finish program
    #any number, milliseconds to wait
    cv2.waitKey(10000)
    cv2.destroyAllWindows()
    
    


if __name__=='__main__':
    print(camera(r'C:\Users\CIDETYS-AIP\Desktop\INDIN_2023\images\t2.jpeg'))
    # camera()