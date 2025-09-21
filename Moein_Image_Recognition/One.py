import os
import cv2

img=cv2.imread('jerry-zhang-nxu_VUcBVdA-unsplash.jpg')
cv2.imshow('img', img)
cv2.waitKey(0)


cv2.imwrite('jerry-zhang-nxu_VUcBVdA-unsplash.png',img)



gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow('gray',gray)
cv2.waitKey(0)
cv2.imwrite('gray.png',gray)

resizes=cv2.resize(img,(300,200))
cv2.imshow('resized',resizes)
cv2.waitKey(0)
cv2.imwrite('resizes.png',resizes)


croped = img[200:300,100:400]
cv2.imshow('croped',croped)
cv2.waitKey(0)
cv2.imwrite('croped.png',croped)



rotated_90 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE) 
cv2.imshow('rotated_90',rotated_90)
cv2.waitKey(0)
cv2.imwrite('rotated_90.png',rotated_90)



rotated_180 = cv2.rotate(img, cv2.ROTATE_180)
cv2.imshow('rotated_180',rotated_180)
cv2.waitKey(0)
cv2.imwrite('rotated_180',rotated_180)


