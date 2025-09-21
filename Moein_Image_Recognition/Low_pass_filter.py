import numpy as np
import cv2
import matplotlib.pyplot as plt

# مرحله 1: خواندن تصویر به صورت خاکستری
img = cv2.imread(r"C:\Users\dehmi\OneDrive\Documents\Desktop\Main\moein\9afe5b4113_yessirsupra-vsthemesorg-fantasy-03.jpg", cv2.IMREAD_GRAYSCALE)

# مرحله 2: تبدیل فوریه دوبعدی
f = np.fft.fft2(img)

# مرحله 3: انتقال فرکانس‌های پایین به مرکز
fshift = np.fft.fftshift(f)

# 🔥 ایجاد ماسک پایین‌گذر دایره‌ای
rows, cols = img.shape              # ابعاد تصویر
crow, ccol = rows // 2 , cols // 2   # مرکز تصویر
radius = 30                          # شعاع ناحیه عبور

mask = np.zeros((rows, cols), np.uint8)           # ماسک صفر
cv2.circle(mask, (ccol, crow), radius, 1, -1)     # دایره پر به مرکز مرکز تصویر

# مرحله 4: اعمال ماسک (ضرب نقطه به نقطه در طیف فوریه)
fshift_filtered = fshift * mask

# مرحله 5: انتقال معکوس برای بازسازی
f_ishift = np.fft.ifftshift(fshift_filtered)

# مرحله 6: تبدیل فوریه معکوس برای بازسازی تصویر
img_back = np.fft.ifft2(f_ishift)

# چون ifft مقادیر مختلط میده => قدر مطلق می‌گیریم
img_back = np.abs(img_back)

# 🎨 نمایش نتایج
plt.figure(figsize=(15,5))

plt.subplot(131)
plt.imshow(img, cmap='gray')
plt.title('Original Image')

plt.subplot(132)
plt.imshow(mask*255, cmap='gray')    # mask*255 فقط برای بهتر دیده شدن
plt.title('Low Pass Mask')

plt.subplot(133)
plt.imshow(img_back, cmap='gray')
plt.title('Low Pass Filtered Image')

plt.show()
