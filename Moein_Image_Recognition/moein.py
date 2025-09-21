import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def detect_circles_with_blur(image_path):
    # Load image
    original = cv2.imread(image_path)
    if original is None:
        print("Error: Image not found or invalid format")
        return None
    
    # Convert to grayscale
    #gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    
    # 1. Advanced Blurring Technique
    # Step 1: Strong Gaussian blur to eliminate noise

    # Step 3: Median blur to eliminate salt-and-pepper noise
    blurred_final = cv2.medianBlur(original, 31)
    
    # 2. Adaptive Thresholding
    adaptive = cv2.adaptiveThreshold(blurred_final, 255, 
                                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                    cv2.THRESH_BINARY_INV, 1001, 7)
    
    # 3. Morphological Processing
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,9))
    closed = cv2.morphologyEx(adaptive, cv2.MORPH_CLOSE, kernel, iterations=3)
    opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel, iterations=2)
    
    # 4. Contour-Based Circle Detection
    contours, _ = cv2.findContours(opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Process contours
    output = original.copy()
    valid_circles = []
    min_radius = 10
    max_radius = 300
    
    for contour in contours:
        # Skip small contours
        if cv2.contourArea(contour) < 100:
            continue
            
        # Fit circle
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius)
        
        # Validate radius
        if radius < min_radius or radius > max_radius:
            continue
            
        # Calculate circularity
        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            continue
        area = cv2.contourArea(contour)
        circularity = 4 * np.pi * area / (perimeter ** 2)
        
        # Validate circularity
        if 0.7 < circularity < 1.3:
            # Check overlap with existing circles
            overlap = False
            for (cx, cy, cr) in valid_circles:
                distance = np.sqrt((x - cx)**2 + (y - cy)**2)
                if distance < (radius + cr) * 0.6:
                    overlap = True
                    break
            
            if not overlap:
                valid_circles.append((x, y, radius))
    
    # Draw valid circles
    circle_count = 0
    for (x, y, r) in valid_circles:
        cv2.circle(output, (int(x), int(y)), r, (0, 255, 0), 3)
        cv2.circle(output, (int(x), int(y)), 2, (0, 0, 255), 3)
        circle_count += 1
    
    # Visualization
    plt.figure(figsize=(15, 10))
    
    # Original image
    plt.subplot(2, 3, 1)
    plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')
    plt.axis('off')
    
    # Blurring stages
    plt.subplot(2, 3, 2)
    plt.imshow(blurred1, cmap='gray')
    plt.title('Gaussian Blur')
    plt.axis('off')
    
    plt.subplot(2, 3, 3)
    plt.imshow(blurred2, cmap='gray')
    plt.title('Bilateral Blur')
    plt.axis('off')
    
    plt.subplot(2, 3, 4)
    plt.imshow(blurred_final, cmap='gray')
    plt.title('Final Blurred Image')
    plt.axis('off')
    
    # Morphological result
    plt.subplot(2, 3, 5)
    plt.imshow(opened, cmap='gray')
    plt.title('Morphological Processing')
    plt.axis('off')
    
    # Final result
    plt.subplot(2, 3, 6)
    plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
    plt.title(f'Detected Circles: {circle_count}')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    print(f"Detected {circle_count} circles")
    return circle_count, output

# Main program
print("===== Circle Detection with Advanced Blurring =====")
print("Please select an image file...")
Tk().withdraw()
file_path = askopenfilename(title='Select image file')

if file_path:
    print("Processing image with advanced blurring...")
    count, result_img = detect_circles_with_blur(file_path)
    cv2.imwrite("blur_detection_result.jpg", result_img)
    print(f"Analysis complete. Found {count} circles. Result saved as 'blur_detection_result.jpg'")
else:
    print("No image selected. Program terminated.")