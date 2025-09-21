import numpy as np
import cv2
import matplotlib.pyplot as plt

# خواندن تصویر خاکستری
img = cv2.imread(r"C:\Users\dehmi\OneDrive\Documents\Desktop\Main\moein\9afe5b4113_yessirsupra-vsthemesorg-fantasy-03.jpg", cv2.IMREAD_GRAYSCALE)

# تبدیل فوریه
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)

# ایجاد ماسک بالاگذر
rows, cols = img.shape
crow, ccol = rows // 2 , cols // 2
radius = 30

# اول یک ماسک پر از یک می‌سازیم
mask = np.ones((rows, cols), np.uint8)

# سپس یک دایره صفر وسطش رسم می‌کنیم (جلوگیری از عبور فرکانس‌های پایین)
cv2.circle(mask, (ccol, crow), radius, 0, -1)

# اعمال ماسک بالاگذر
fshift_filtered = fshift * mask

# تبدیل فوریه معکوس
f_ishift = np.fft.ifftshift(fshift_filtered)
img_back = np.fft.ifft2(f_ishift)
img_back = np.abs(img_back)

# نمایش نتایج
plt.figure(figsize=(15,5))

plt.subplot(131)
plt.imshow(img, cmap='gray')
plt.title('Original Image')

plt.subplot(132)
plt.imshow(mask*255, cmap='gray')
plt.title('High Pass Mask')

plt.subplot(133)
plt.imshow(img_back, cmap='gray')
plt.title('High Pass Filtered Image')

plt.show()
