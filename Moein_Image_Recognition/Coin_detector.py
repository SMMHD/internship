import cv2
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog

# Hide the main Tkinter window
root = tk.Tk()
root.withdraw()

# Open file selection dialog
image_path = filedialog.askopenfilename(
    title="Select an image",
    filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff")]
)

if not image_path:
    print("No image selected. Exiting.")
    exit()

# Load and convert image
img = cv2.imread(image_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Show original image
plt.figure(figsize=(8, 6))
plt.imshow(img_rgb)
plt.title("Step 1: Input Image")
plt.axis('off')
plt.show()

# Step 2: Convert to Grayscale and Apply Gaussian Blur
gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (151, 151), 0)

plt.figure(figsize=(8, 6))
plt.imshow(blurred, cmap='gray')
plt.title("Step 2: Grayscale + Gaussian Blur")
plt.axis('off')
plt.show()

# Step 3: Edge Detection
edges = cv2.Canny(gray, 30, 100)
combined = cv2.addWeighted(blurred, 1, edges, 1, 0)

edges = cv2.Canny(gray, 60, 150)
combined = cv2.addWeighted(blurred, 1, edges, 0.4, 0)

# Step 4: Global Thresholding
_, thresh = cv2.threshold(blurred, 233, 255, cv2.THRESH_BINARY_INV)

plt.figure(figsize=(8, 6))
plt.imshow(thresh, cmap='gray')
plt.title("Step 3: Global Thresholding")
plt.axis('off')
plt.show()

# Step 5.1: Morphological Closing
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

# Step 5.2: Morphological Opening (Noise Removal)
opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel, iterations=1)

# Step 5.3: Distance Transform
dist_transform = cv2.distanceTransform(opened, cv2.DIST_L2, 5)
_, sure_fg = cv2.threshold(dist_transform, 0.6 * dist_transform.max(), 255, 0)
sure_fg = np.uint8(sure_fg)

# Step 5.4: Sure Background
sure_bg = cv2.dilate(opened, kernel, iterations=3)
unknown = cv2.subtract(sure_bg, sure_fg)

# Step 5.5: Marker Labelling
_, markers = cv2.connectedComponents(sure_fg)
markers = markers + 1
markers[unknown == 255] = 0

# Step 6: Apply Watershed
image_watershed = img_rgb.copy()
markers = cv2.watershed(image_watershed, markers)

# Step 7: Detect Boundaries
boundary_mask = np.uint8(markers == -1)
contours, _ = cv2.findContours(boundary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(image_watershed, contours, -1, (0, 0, 255), 5)

# Step 8: Label Each Coin
font = cv2.FONT_HERSHEY_SIMPLEX
for label in range(2, markers.max() + 1):
    mask = np.uint8(markers == label)
    M = cv2.moments(mask)
    if M["m00"] > 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        cv2.putText(image_watershed, str(label - 1), (cx - 30, cy + 10),
                    font, 5.0, (0, 255, 0), 10, cv2.LINE_AA)

# Count Number of Coins
num_coins = markers.max() - 1

# Final Result
plt.figure(figsize=(10, 8))
plt.imshow(cv2.cvtColor(image_watershed, cv2.COLOR_BGR2RGB))
plt.title(f"Step 4: Detected Coins with Watershed - Count: {num_coins}")
plt.axis('off')
plt.show()

print("Number of coins detected:", num_coins)
