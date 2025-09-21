import pandas as pd
from PIL import Image
import os
from pathlib import Path

# --- Configuration ---
excel_file_path = Path(r"H:\Hosseini\dataset\xlx\tt2.xlsx")
images_folder = Path(r"H:\Hosseini\dataset\Images orginal size")
labels_folder = Path(r"C:\Users\dehmi\OneDrive\Documents\Desktop\lable yolo")

# Define class names and class IDs
class_name_to_id = {
    'eshpil': 0,
    'keshpil': 1,
    'neshpil': 2,
    'eshpilkm': 3,
}

# --- Create labels folder if it doesn't exist ---
labels_folder.mkdir(parents=True, exist_ok=True)

# --- Load data from Excel file ---
try:
    df = pd.read_excel(excel_file_path, header=None)
    x1 = df.iloc[:, 1].values
    y1 = df.iloc[:, 2].values
    x2 = df.iloc[:, 3].values
    y2 = df.iloc[:, 4].values
    image_base_names = df.iloc[:, 0].values
    classes_str = df.iloc[:, 5].values
    label_file_names = df.iloc[:, 6].values
except FileNotFoundError:
    print(f"Error: Excel file not found at '{excel_file_path}'")
    exit()
except Exception as e:
    print(f"Error reading Excel file: {e}")
    exit()

# --- Process each entry ---
for i in range(len(x1)):
    try:
        image_base_name = image_base_names[i]
        
        # Determine the correct image path by checking for various extensions and double extensions
        image_path = None
        possible_extensions = ['', '.jpg', '.jpeg', '.JPG', '.JPEG']
        
        # The empty string allows for cases like 'image.jpg' where the extension is already in the name
        for ext in possible_extensions:
            temp_path = images_folder / f"{image_base_name}{ext}"
            if temp_path.is_file():
                image_path = temp_path
                break
            
            # This handles the 'double extension' case like 'filename.jpg.jpg'
            # It checks if the base name already ends with a common image extension
            if image_base_name.lower().endswith(('.jpg', '.jpeg')):
                temp_path = images_folder / image_base_name
                if temp_path.is_file():
                    image_path = temp_path
                    break

        if image_path is None:
            print(f"Warning: Image file not found for '{image_base_name}'. Skipping.")
            continue

        # Open image to get dimensions
        with Image.open(image_path) as img:
            width_img, height_img = img.size

        # Normalize the class name by stripping whitespace and converting to lowercase
        # This helps in matching class names even if there are slight variations in spelling/case
        class_name = str(classes_str[i]).strip().lower() 
        class_id = class_name_to_id.get(class_name)

        if class_id is None:
            # If a normalized class name is still not found, print an error and skip
            print(f"Error: Invalid class name '{classes_str[i]}' (normalized to '{class_name}') found for image '{image_base_name}'. "
                  f"Please update 'class_name_to_id' dictionary with this class or correct the Excel data. Skipping this entry.")
            continue # Skip to the next entry instead of exiting

        # Calculate normalized bounding box parameters
        xcen = ((x1[i] + x2[i]) / 2) / width_img
        ycen = ((y1[i] + y2[i]) / 2) / height_img
        width_bbox = (x2[i] - x1[i]) / width_img
        height_bbox = (y2[i] - y1[i]) / height_img

        # Prepare YOLOv5 format label string
        label_data_str = f"{class_id} {xcen:.6f} {ycen:.6f} {width_bbox:.6f} {height_bbox:.6f}"

        # Write label to file
        label_filename = f"{label_file_names[i]}.txt"
        output_label_path = labels_folder / label_filename

        # Use 'w' mode for writing to ensure each image's label file is created/overwritten correctly
        # If you intend to append multiple bounding boxes to the same file for an image, use 'a'
        # Given your error log, it seems you might have multiple entries for the same image/label file,
        # so 'a' (append) might be intentional. I'll keep 'a' as per your original code.
        with open(output_label_path, 'a') as f:
            f.write(label_data_str + '\n')
            
        print(f"Successfully wrote label for '{image_path.name}' to '{label_filename}'")

    except Exception as e:
        print(f"Error processing entry {i} (Image: {image_base_names[i]}): {e}")

print("\nLabel generation complete!")
