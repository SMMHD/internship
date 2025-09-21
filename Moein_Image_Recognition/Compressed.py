import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read the image in BGR and convert to RGB
image_bgr = cv2.imread(r"C:\Users\dehmi\OneDrive\Documents\Desktop\Main\moein\9afe5b4113_yessirsupra-vsthemesorg-fantasy-03.jpg")
image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

# Get image dimensions
rows, cols, _ = image.shape
crow, ccol = rows // 2 , cols // 2
radius = 150  # Radius for low-pass filter

# Create circular low-pass filter mask
mask = np.zeros((rows, cols), np.uint8)
cv2.circle(mask, (ccol, crow), radius, 1, thickness=-1)

# Function to filter a single color channel
def filter_channel(channel):
    f = np.fft.fft2(channel)
    fshift = np.fft.fftshift(f)
    fshift_filtered = fshift * mask
    f_ishift = np.fft.ifftshift(fshift_filtered)
    img_back = np.fft.ifft2(f_ishift)
    return np.abs(img_back)

# Split image into color channels
R, G, B = cv2.split(image)

# Apply low-pass filter to each channel
R_filtered = filter_channel(R)
G_filtered = filter_channel(G)
B_filtered = filter_channel(B)

# Merge filtered channels back into RGB image
image_filtered = cv2.merge((R_filtered.astype(np.uint8),
                            G_filtered.astype(np.uint8),
                            B_filtered.astype(np.uint8)))

# Display original and filtered images
plt.figure(figsize=(10,5))
plt.subplot(1,2,1)
plt.imshow(image)
plt.title('Original Image (RGB)')
plt.axis('off')

plt.subplot(1,2,2)
plt.imshow(image_filtered)
plt.title('Compressed Image (Low-pass RGB)')
plt.axis('off')

plt.tight_layout()
plt.show()
