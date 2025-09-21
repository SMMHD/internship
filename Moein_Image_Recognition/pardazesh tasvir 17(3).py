import cv2
import numpy as np
import matplotlib.pyplot as plt

# بارگذاری تصویر
image_path = r'C:\Users\KRIPL\Downloads\coin4.jpg' # یا مسیر کامل فایل تصویر
image = cv2.imread(image_path)

# تبدیل به سطح خاکستری
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# حذف نویز با Gaussian Blur
blurred = cv2.GaussianBlur(gray, (11, 11), 0)

# آستانه‌گذاری تطبیقی برای باینری کردن تصویر
thresh = cv2.adaptiveThreshold(blurred, 255,
                               cv2.ADAPTIVE_THRESH_MEAN_C,
                               cv2.THRESH_BINARY_INV, 11, 3)

# عملیات مورفولوژی برای بستن فضاهای خالی داخل سکه‌ها
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

# یافتن کانتورهای خارجی
contours, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# فیلتر کردن کانتورهای کوچک که نویز هستند
min_coin_area = 500
coin_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_coin_area]

# رسم کانتورها روی تصویر اصلی
output_image = image.copy()
cv2.drawContours(output_image, coin_contours, -1, (0, 255, 0), 2)

# چاپ تعداد سکه‌ها
print("تعداد سکه‌ها:", len(coin_contours))

# نمایش تصویر نهایی (با matplotlib برای محیط‌های Jupyter یا IDE)
output_rgb = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(10, 8))
plt.imshow(output_rgb)
plt.title(f"تعداد سکه‌ها: {len(coin_contours)}")
plt.axis('off')
plt.show()
