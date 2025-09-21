import cv2
import os 
import numpy as np
import subprocess


image = cv2.imread(os.path.join('jerry-zhang-nxu_VUcBVdA-unsplash.jpg'))


blurred_image = cv2.GaussianBlur(image, (5,5), 0) 

cv2.imwrite('blurred_imag.tiff',blurred_image)


# player_path = 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PotPlayer'  
# image_path = 'jerry-zhang-nxu_VUcBVdA-unsplash.jpg'

# subprocess.Popen([player_path, image_path])

#cv2.imshow('Original Image', image)
#cv2.waitKey(50000)





b, g, r = cv2.split(image)


cv2.imwrite('blue_channel.tiff', b)
cv2.imwrite('green_channel.tiff', g)
cv2.imwrite('red_channel.tiff', r)


#cv2.imshow('Blue Channel', b)
cv2.waitKey(0)
#cv2.imshow('Green Channel', g)
#cv2.waitKey(0)
#cv2.imshow('Red Channel', r)
cv2.waitKey(0)





#cv2.imshow('Blurred Image', blurred_image)
cv2.waitKey(0)




gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite('gray_image.tiff',gray_image)
#cv2.imshow('gray_image', gray_image)
#cv2.waitKey(0)


kernel = np.array([[-1, -1, -1],
                   [-1,  9, -1],
                   [-1, -1, -1]])
sharpened_image = cv2.filter2D(image, -1, kernel)


cv2.imwrite('sharpened_image.tiff',sharpened_image)
#cv2.imshow('sharpened_image', sharpened_image)
#cv2.waitKey(0)


kernel = np.array([[-2, -1, 0],
                   [-1,  1, 1],
                   [ 0,  1, 2]])
embossed_image = cv2.filter2D(image, -1, kernel)

cv2.imwrite('embossed_image.tiff',embossed_image)
#cv2.imshow('embossed_image', embossed_image)
#cv2.waitKey(0)


a=cv2.imread(os.path.join('blue_channel.tiff'))
v=cv2.imread(os.path.join('blurred_imag.tiff'))
c=cv2.imread(os.path.join('embossed_image.tiff'))
d=cv2.imread(os.path.join('gray_image.tiff'))
e=cv2.imread(os.path.join('green_channel.tiff'))
f=cv2.imread(os.path.join('jerry-zhang-nxu_VUcBVdA-unsplash.jpg'))
g=cv2.imread(os.path.join('red_channel.tiff'))
h=cv2.imread(os.path.join('sharpened_image.tiff'))

desired_size = (150, 150)  

a = cv2.resize(a, desired_size)
v = cv2.resize(v, desired_size)
c = cv2.resize(c, desired_size)
d = cv2.resize(d, desired_size)
e = cv2.resize(e, desired_size)
f = cv2.resize(f, desired_size)
g = cv2.resize(g, desired_size)
h = cv2.resize(h, desired_size)


#horizontal_concat = cv2.hconcat([image,b ,g,r,blurred_image,gray_image,sharpened_image,embossed_image ])

m = cv2.hconcat([a,v ,c,d,e,f,g,h])

cv2.imshow('Combined Image', m)
cv2.waitKey(0)



cv2.destroyAllWindows()
print("hello")

#cv2.imwrite('blurred_image.jpg', blurred_image)

