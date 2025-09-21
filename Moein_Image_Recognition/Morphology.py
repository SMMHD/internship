import cv2
import numpy as np
from matplotlib import pyplot as plt

# خواندن تصویر به صورت سیاه و سفید
img = cv2.imread(r"C:\Users\dehmi\Downloads\gettyimages-2157824079-2048x2048.jpg", 0)

# باینری کردن تصویر (Thresholding)
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# ایجاد یک structuring element (kernel)
kernel = np.ones((5,5), np.uint8)

# عملیات‌های مورفولوژیک
erosion = cv2.erode(binary, kernel, iterations=1)
dilation = cv2.dilate(binary, kernel, iterations=1)
opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

# نمایش نتایج
titles = ['Original', 'Binary', 'Erosion', 'Dilation', 'Opening', 'Closing']
images = [img, binary, erosion, dilation, opening, closing]

plt.figure(figsize=(15,8))  # بزرگ‌تر کردن figure

for i in range(6):
    plt.subplot(2, 3, i+1)  # نمایش در یک شبکه 2×3
    plt.imshow(images[i], cmap='gray')
    plt.title(titles[i], fontsize=14)  # عنوان با فونت بزرگ‌تر
    plt.axis('off')

plt.tight_layout(pad=2.0)  # فاصله مناسب بین تصاویر
plt.show()
