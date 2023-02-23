###does an object detection and squares de object

import cv2
import numpy as np

empty=cv2.imread('./images/empty.jpg')
case=cv2.imread('./images/case.jpg')
key=cv2.imread('./images/key.jpg')
wallet=cv2.imread('./images/wallet.jpg')

emptys=cv2.resize(empty,(960,540)) #: resized image
cases=cv2.resize(case,(960,540)) #: resized image


cv2.imshow('prueba',emptys)


cv2.waitKey(0)
cv2.destroyAllWindows()
