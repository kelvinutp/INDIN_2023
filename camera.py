##gets image from a camera and displays it on the screen

# import the opencv library
import cv2

# define a video capture object
vid = cv2.VideoCapture(0)

#read image
result, image = vid.read()

if result:
    #display image
    cv2.imshow('prueba',image)

    #press any key to finish program
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print('no image')
