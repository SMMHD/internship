import cv2
import numpy as np
import matplotlib.pyplot as plt

# خواندن تصویر
image = cv2.imread(r"C:\Users\dehmi\Downloads\images\creative-portrait-beautiful-woman.jpg")

# جدا کردن کانال‌ها
B, G, R = cv2.split(image)

# ------------------------
# پردازش Sobel
def apply_sobel(channel):
    sobelx = cv2.Sobel(channel, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(channel, cv2.CV_64F, 0, 1, ksize=3)
    sobel = cv2.magnitude(sobelx, sobely)
    sobel = np.uint8(np.clip(sobel, 0, 255))
    return sobel

sobel_R = apply_sobel(R)
sobel_G = apply_sobel(G)
sobel_B = apply_sobel(B)

merged_sobel = cv2.merge([sobel_B, sobel_G, sobel_R])

# ------------------------
# پردازش Canny
def apply_canny(channel):
    canny = cv2.Canny(channel, 100, 200)
    return canny

canny_R = apply_canny(R)
canny_G = apply_canny(G)
canny_B = apply_canny(B)

merged_canny = cv2.merge([canny_B, canny_G, canny_R])

# ------------------------
# پردازش Laplacian
def apply_laplacian(channel):
    laplacian = cv2.Laplacian(channel, cv2.CV_64F)
    laplacian = np.uint8(np.absolute(laplacian))
    return laplacian

laplacian_R = apply_laplacian(R)
laplacian_G = apply_laplacian(G)
laplacian_B = apply_laplacian(B)

merged_laplacian = cv2.merge([laplacian_B, laplacian_G, laplacian_R])

# ------------------------
# نمایش نتایج در کنار هم
plt.figure(figsize=(18,6))

plt.subplot(1,3,1)
plt.imshow(cv2.cvtColor(merged_sobel, cv2.COLOR_BGR2RGB))
plt.title('Sobel on RGB channels')
plt.axis('off')

plt.subplot(1,3,2)
plt.imshow(cv2.cvtColor(merged_canny, cv2.COLOR_BGR2RGB))
plt.title('Canny on RGB channels')
plt.axis('off')

plt.subplot(1,3,3)
plt.imshow(cv2.cvtColor(merged_laplacian, cv2.COLOR_BGR2RGB))
plt.title('Laplacian on RGB channels')
plt.axis('off')

plt.tight_layout()
plt.show()
