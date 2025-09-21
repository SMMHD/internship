import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# مسیر فایل‌ها
input_path = r"C:\Users\dehmi\OneDrive\Documents\Desktop\Main\moein\9afe5b4113_yessirsupra-vsthemesorg-fantasy-03.jpg"
output_path = "compressed_output.jpg"

# خواندن تصویر اصلی به صورت رنگی (BGR → RGB)
image_bgr = cv2.imread(input_path)
image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

# ابعاد تصویر
rows, cols, _ = image.shape
crow, ccol = rows // 2, cols // 2
radius = 150  # شعاع فیلتر

# ماسک پایین‌گذر
mask = np.zeros((rows, cols), np.uint8)
cv2.circle(mask, (ccol, crow), radius, 1, thickness=-1)

# تابع فیلتر فوریه برای یک کانال
def filter_channel(channel):
    f = np.fft.fft2(channel)
    fshift = np.fft.fftshift(f)
    fshift_filtered = fshift * mask
    f_ishift = np.fft.ifftshift(fshift_filtered)
    img_back = np.fft.ifft2(f_ishift)
    return np.abs(img_back)

# جدا کردن کانال‌ها و فیلتر آن‌ها
R, G, B = cv2.split(image)
R_filtered = filter_channel(R)
G_filtered = filter_channel(G)
B_filtered = filter_channel(B)

# ترکیب کانال‌ها و تبدیل به uint8
filtered_image = cv2.merge((
    R_filtered.astype(np.uint8),
    G_filtered.astype(np.uint8),
    B_filtered.astype(np.uint8)
))

# تبدیل به BGR و ذخیره با کیفیت پایین‌تر (JPEG)
filtered_bgr = cv2.cvtColor(filtered_image, cv2.COLOR_RGB2BGR)
cv2.imwrite(output_path, filtered_bgr, [cv2.IMWRITE_JPEG_QUALITY, 60])

# محاسبه حجم فایل‌ها
size_original = os.path.getsize(input_path) / 1024  # KB
size_compressed = os.path.getsize(output_path) / 1024  # KB

# نمایش دو تصویر کنار هم با حجم فایل
compressed_image = cv2.cvtColor(cv2.imread(output_path), cv2.COLOR_BGR2RGB)

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(image)
plt.title(f'Original Image\nSize: {size_original:.2f} KB')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(compressed_image)
plt.title(f'Compressed Image\nSize: {size_compressed:.2f} KB')
plt.axis('off')

plt.tight_layout()
plt.show()
