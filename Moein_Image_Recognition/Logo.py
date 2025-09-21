import cv2
import os
import numpy as np
import matplotlib.pyplot as plt




#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# خواندن تصویر اصلی
img = cv2.imread(r'G:\ax\photo_2024-09-28_19-34-46.jpg')
if img is None:
    raise ValueError("تصویر اصلی خوانده نشد! آدرس را بررسی کن.")

# خواندن لوگو با آلفا
logo = cv2.imread(r'F:\University\6th term\Rayan_Pajoohesh.jpg', cv2.IMREAD_UNCHANGED)
if logo is None:
    raise ValueError("لوگو خوانده نشد! آدرس را بررسی کن.")

# جدا کردن BGR و آلفا
if logo.shape[2] == 4:
    logo_bgr = logo[:, :, :3]
    print()
    alpha = logo[:, :, 3] / 255.0
else:
    logo_bgr = logo
    a=logo_bgr.shape
    alpha = np.ones(logo_bgr.shape[:2], dtype=float)

# تغییر اندازه لوگو به 20 درصد عرض تصویر اصلی
scale = 0.2
new_w = int(img.shape[1] * scale)
new_h = int(logo_bgr.shape[0] * new_w / logo_bgr.shape[1])

logo_bgr = cv2.resize(logo_bgr, (new_w, new_h), interpolation=cv2.INTER_AREA)
alpha = cv2.resize(alpha, (new_w, new_h), interpolation=cv2.INTER_AREA)

# اطمینان از شکل آلفا برای broadcast
if len(alpha.shape) == 2:
    alpha = alpha[..., np.newaxis]  # تبدیل به (h, w, 1)

# مکان قرارگیری: پایین-راست
x = img.shape[1] - new_w - 10
y = img.shape[0] - new_h - 10

# گرفتن ROI از تصویر اصلی
roi = img[y:y+new_h, x:x+new_w]

# ترکیب لوگو با ROI
roi = (alpha * logo_bgr + (1 - alpha) * roi).astype(np.uint8)

# قرار دادن دوباره در تصویر اصلی
img[y:y+new_h, x:x+new_w] = roi

# تبدیل BGR به RGB برای نمایش زیباتر با matplotlib
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# نمایش
plt.figure(figsize=(10, 8))
plt.imshow(img_rgb)
plt.axis('off')
plt.title("Result", fontsize=16)
plt.show()
