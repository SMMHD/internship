import cv2
import numpy as np
from tkinter import Tk, filedialog
from tkinter import simpledialog

def select_image():
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")]
    )
    root.destroy()
    return file_path

def detect_circles():
    # Let user select image
    image_path = select_image()
    if not image_path:
        print("No image selected")
        return
    
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        print("Error loading image")
        return
    
    # Get user parameters
    root = Tk()
    root.withdraw()
    min_size = simpledialog.askinteger("Parameters", "Minimum circle size (pixels):", initialvalue=50)
    max_size = simpledialog.askinteger("Parameters", "Maximum circle size (pixels):", initialvalue=500)
    root.destroy()
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive threshold
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                 cv2.THRESH_BINARY_INV, 11, 2)
    
    # Morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel, iterations=2)
    
    # Find contours
    contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Detect circles
    result = img.copy()
    circles = []
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_size or area > max_size:
            continue
            
        perimeter = cv2.arcLength(cnt, True)
        if perimeter == 0:
            continue
            
        circularity = 4 * np.pi * area / (perimeter**2)
        if 0.75 < circularity < 1.25:  # Circle range
            (x,y), radius = cv2.minEnclosingCircle(cnt)
            center = (int(x), int(y))
            radius = int(radius)
            circles.append((center, radius))
    
    # Draw results
    for (center, radius) in circles:
        cv2.circle(result, center, radius, (0,255,0), 2)
        cv2.circle(result, center, 2, (0,0,255), 3)
    
    # Resize for display if too large
    scale = min(800/img.shape[1], 600/img.shape[0])
    if scale < 1:
        display_img = cv2.resize(result, (0,0), fx=scale, fy=scale)
    else:
        display_img = result
    
    # Show results
    cv2.imshow(f"Detected {len(circles)} Circles", display_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_circles()