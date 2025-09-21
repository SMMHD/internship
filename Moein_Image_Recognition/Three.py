import cv2
import os
import numpy as np
import matplotlib.pyplot as plt 

def process_and_display_image_grid_matplotlib(image_path):

    image = cv2.imread(image_path)

    if image is None:
        print(f"خطا: فایل تصویر '{image_path}' پیدا نشد یا بارگذاری نشد.")
        return

    processed_images = []
    titles = []
    desired_size = (500,500) 

   
    # نکته: برای نمایش در Matplotlib، تصاویر BGR باید به RGB تبدیل شوند
    original_resized_rgb = cv2.resize(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), desired_size)
    processed_images.append(original_resized_rgb)
    titles.append('Original')



    # 2.1. Gaussian Blur (محو کردن گوسی)
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
    processed_images.append(cv2.resize(cv2.cvtColor(blurred_image, cv2.COLOR_BGR2RGB), desired_size))
    titles.append('Gaussian Blur')

    # 2.2. Median Blur (محو کردن میانه - برای حذف نویزهای نمک و فلفل)
    median_blurred_image = cv2.medianBlur(image, 5) # اندازه کرنل
    processed_images.append(cv2.resize(cv2.cvtColor(median_blurred_image, cv2.COLOR_BGR2RGB), desired_size))
    titles.append('Median Blur')

    # 2.3. Gray Image (تصویر خاکستری)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    processed_images.append(cv2.resize(gray_image, desired_size))
    titles.append('Grayscale')

    # 2.4. Sharpened Image (واضح سازی)
    kernel_sharpen = np.array([[-1, -1, -1],
                               [-1,  9, -1],
                               [-1, -1, -1]])
    sharpened_image = cv2.filter2D(image, -1, kernel_sharpen)
    processed_images.append(cv2.resize(cv2.cvtColor(sharpened_image, cv2.COLOR_BGR2RGB), desired_size))
    titles.append('Sharpened')

    # 2.5. Embossed Image (برجسته سازی)
    kernel_emboss = np.array([[-2, -1, 0],
                              [-1,  1, 1],
                              [ 0,  1, 2]])
    embossed_image = cv2.filter2D(image, -1, kernel_emboss)
    processed_images.append(cv2.resize(cv2.cvtColor(embossed_image, cv2.COLOR_BGR2RGB), desired_size))
    titles.append('Embossed')
    
   
    edges = cv2.Canny(gray_image, 100, 200)
    processed_images.append(cv2.resize(edges, desired_size)) 
    titles.append('Canny Edges')

    ret, thresholded_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
    processed_images.append(cv2.resize(thresholded_image, desired_size)) 
    titles.append('Threshold Binary')

    b, g, r = cv2.split(image)
    
 
    processed_images.append(cv2.resize(b, desired_size))
    titles.append('Blue Channel')
    processed_images.append(cv2.resize(g, desired_size))
    titles.append('Green Channel')
    processed_images.append(cv2.resize(r, desired_size))
    titles.append('Red Channel')
    

 

    
    num_cols = 4
    num_rows = (len(processed_images) + num_cols - 1) // num_cols

    plt.figure(figsize=(num_cols * 3.5, num_rows * 3.5)) 
    
    for i in range(len(processed_images)):
        plt.subplot(num_rows, num_cols, i + 1) 
        
        
        if len(processed_images[i].shape) == 2: 
            plt.imshow(processed_images[i], cmap='gray')
        else: 
            plt.imshow(processed_images[i])
            
        plt.title(titles[i], fontsize=10) 
        plt.axis('off') 
    plt.tight_layout() 
    plt.show()

    print("پردازش تصاویر به پایان رسید.")


process_and_display_image_grid_matplotlib(r"G:\ax\photo_2024-09-28_19-34-46.jpg")