import cv2
import numpy as np
import matplotlib.pyplot as plt

img1 = cv2.imread(r'G:\ax\photo_2024-09-28_19-34-46.jpg')
img2 = cv2.imread(r'G:\ax\photo_2024-09-28_19-35-25.jpg')

if img1 is None or img2 is None:
    raise ValueError("خطا: یکی از تصاویر پیدا نشد. مسیر فایل‌ها رو چک کن.")

h1, w1 = img1.shape[:2]
h2, w2 = img2.shape[:2]

print(f"ابعاد تصویر اول: {w1}x{h1}")
print(f"ابعاد تصویر دوم: {w2}x{h2}")

if h1 * w1 > h2 * w2:
    img1 = cv2.resize(img1, (w2, h2))
    print("تصویر اول به اندازه تصویر دوم resize شد.")
elif h2 * w2 > h1 * w1:
    img2 = cv2.resize(img2, (w1, h1))
    print("تصویر دوم به اندازه تصویر اول resize شد.")
else:
    print("تصاویر از قبل هم‌سایز هستند.")

sum_image = cv2.add(img1, img2)
diff_image = cv2.subtract(img1, img2)

# تبدیل BGR به RGB برای plt
sum_image_rgb = cv2.cvtColor(sum_image, cv2.COLOR_BGR2RGB)
diff_image_rgb = cv2.cvtColor(diff_image, cv2.COLOR_BGR2RGB)

# نمایش با plt
plt.figure(figsize=(10,5))

plt.subplot(1,2,1)
plt.imshow(sum_image_rgb)
plt.title('Sum Image')
plt.axis('off')

plt.subplot(1,2,2)
plt.imshow(diff_image_rgb)
plt.title('Difference Image')
plt.axis('off')

plt.show()

cv2.imwrite("sum_image.png", sum_image)
cv2.imwrite("diff_image.png", diff_image)
print("✅ تصاویر جمع و تفریق در فایل‌های sum_image.png و diff_image.png ذخیره شدند.")
