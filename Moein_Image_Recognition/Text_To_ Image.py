import cv2
import os

def add_text_to_image(image_path, text, output_path=None):
   
    img = cv2.imread(image_path)

    if img is None:
        print(f"خطا: فایل تصویر '{image_path}' پیدا نشد یا بارگذاری نشد.")
        return


    font = cv2.FONT_HERSHEY_SIMPLEX 
    font_scale = 1.5               
    color = (0, 0, 255)            
    thickness = 2               
    line_type = cv2.LINE_AA        
    (h, w) = img.shape[:2]
    
 
    text_x = 50
    text_y = h - 50 
  
    org = (text_x, text_y) 

    output_img = cv2.putText(img.copy(), text, org, font, font_scale, color, thickness, line_type) 

   
    if output_path is None:
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        ext = os.path.splitext(os.path.basename(image_path))[1]
        output_path = os.path.join(os.path.dirname(image_path), f"{base_name}_with_text{ext}")

    cv2.imwrite(output_path, output_img)
    print(f"تصویر با متن اضافه شده در '{output_path}' ذخیره گردید.")

   
    cv2.imshow('Image with Text', output_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


image_to_process = r'G:\ax\photo_2024-09-28_19-34-46.jpg'
text_to_add = 'Hello OpenCV!'

add_text_to_image(image_to_process, text_to_add)
