import cv2
import numpy as np
import matplotlib.pyplot as plt

# خواندن تصویر
img_bgr = cv2.imread(r'C:\Users\dehmi\Downloads\blue-leaf-border-gray.jpg')
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

# تبدیل به فضاهای رنگی مختلف
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
img_lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
img_ycrcb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YCrCb)

# ساخت لیست داده‌ها
images = [
    ('RGB', img_rgb),
    ('Grayscale', img_gray),
    ('HSV', img_hsv),
    ('LAB', img_lab),
    ('YCrCb', img_ycrcb)
]

# نمایش تصاویر و هیستوگرام‌هایشان
plt.figure(figsize=(18, 20))

for i, (title, image) in enumerate(images):
    # تصویر
    plt.subplot(5, 2, 2 * i + 1)
    if len(image.shape) == 2:
        plt.imshow(image, cmap='gray')
    else:
        plt.imshow(image)
    plt.title(f'{title} Image')
    plt.axis('off')

    # هیستوگرام
    plt.subplot(5, 2, 2 * i + 2)
    if len(image.shape) == 2:
        # Grayscale
        hist = cv2.calcHist([image], [0], None, [256], [0, 256])
        plt.plot(hist, color='black')
    else:
        # رنگی
        colors = ('r', 'g', 'b')
        if title == 'HSV':
            colors = ('y', 'm', 'c')  # برای تفاوت
        elif title == 'LAB':
            colors = ('k', 'orange', 'blue')
        elif title == 'YCrCb':
            colors = ('k', 'r', 'b')

        for j, col in enumerate(colors):
            hist = cv2.calcHist([image], [j], None, [256], [0, 256])
            plt.plot(hist, color=col, label=f'Channel {j}')
    plt.title(f'{title} Histogram')
    plt.xlim([0, 256])
    plt.legend()

plt.tight_layout()
plt.show()





# خواندن تصویر به صورت سیاه و سفید
img_gray = cv2.imread(r'C:\Users\dehmi\Downloads\blue-leaf-border-gray.jpg', 0)

# هیستوگرام اصلی تصویر
hist_original = cv2.calcHist([img_gray], [0], None, [256], [0, 256])

# اعمال Histogram Equalization
equalized = cv2.equalizeHist(img_gray)

# هیستوگرام تصویر بهبود یافته
hist_equalized = cv2.calcHist([equalized], [0], None, [256], [0, 256])

# نمایش تصاویر و هیستوگرام‌ها
plt.figure(figsize=(12, 6))

# تصویر اصلی
plt.subplot(2, 2, 1)
plt.imshow(img_gray, cmap='gray')
plt.title("Original Image")
plt.axis('off')

# هیستوگرام اصلی
plt.subplot(2, 2, 2)
plt.plot(hist_original, color='black')
plt.title("Original Histogram")

# تصویر بهبود یافته
plt.subplot(2, 2, 3)
plt.imshow(equalized, cmap='gray')
plt.title("Equalized Image")
plt.axis('off')

# هیستوگرام جدید
plt.subplot(2, 2, 4)
plt.plot(hist_equalized, color='black')
plt.title("Equalized Histogram")

plt.tight_layout()
plt.show()







import cv2
import numpy as np
from matplotlib import pyplot as plt

# خواندن تصویر رنگی
img_color = cv2.imread(r'C:\Users\dehmi\Downloads\blue-leaf-border-gray.jpg')
img_lab = cv2.cvtColor(img_color, cv2.COLOR_BGR2LAB)

# جدا کردن کانال‌ها
l, a, b = cv2.split(img_lab)

# اعمال CLAHE فقط روی کانال L
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
l_clahe = clahe.apply(l)

# بازترکیب کانال‌ها
lab_clahe = cv2.merge((l_clahe, a, b))
img_clahe = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)

# رسم نتایج
plt.figure(figsize=(12,8))

# نمایش تصویر اصلی
plt.subplot(2,2,1)
plt.imshow(cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB))
plt.title("Original Color Image")
plt.axis('off')

# نمایش تصویر بهبود یافته
plt.subplot(2,2,2)
plt.imshow(cv2.cvtColor(img_clahe, cv2.COLOR_BGR2RGB))
plt.title("CLAHE Enhanced")
plt.axis('off')

# رسم هیستوگرام L قبل
plt.subplot(2,2,3)
plt.hist(l.ravel(), bins=256, range=[0,256], color='gray')
plt.title('Histogram of L channel (Original)')
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')

# رسم هیستوگرام L بعد
plt.subplot(2,2,4)
plt.hist(l_clahe.ravel(), bins=256, range=[0,256], color='gray')
plt.title('Histogram of L channel (CLAHE)')
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()











