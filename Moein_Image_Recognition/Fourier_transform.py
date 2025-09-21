import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread(r"C:\Users\dehmi\OneDrive\Documents\Desktop\Main\moein\9afe5b4113_yessirsupra-vsthemesorg-fantasy-03.jpg", cv2.IMREAD_GRAYSCALE)

# تبدیل فوریه دوبعدی
f = np.fft.fft2(img)
# انتقال فرکانس‌های پایین به مرکز
fshift = np.fft.fftshift(f)

# محاسبه دامنه
magnitude_spectrum = 20*np.log(np.abs(fshift))


plt.subplot(121), plt.imshow(img, cmap='gray'), plt.title('Original Image')
plt.subplot(122), plt.imshow(magnitude_spectrum, cmap='gray'), plt.title('Magnitude Spectrum')
plt.show()



# انتقال برعکس
f_ishift = np.fft.ifftshift(fshift)
# معکوس فوریه
img_back = np.fft.ifft2(f_ishift)
# فقط قسمت حقیقی
img_back = np.abs(img_back)

plt.imshow(img_back, cmap='gray')
plt.title('Reconstructed Image')
plt.show()
