import pandas as pd
from PIL import Image
import os
import json
from pathlib import Path
import re

# --- Configuration ---
# Update these paths to match your system
excel_file_path = Path(r"H:\Hosseini\dataset\xlx\tt..xlsx")
images_folder = Path(r"H:\Hosseini\dataset\Compressed images")
output_json_file = Path(r"H:\Hosseini\dataset\annotations.coco.json")

# Mapping of class names to their corresponding integer IDs
class_name_to_id = {
    'eshpil': 0,
    'keshpli': 1,
    'neshpil': 2,
    'eshpilkm': 3,
}

# --- Initialize COCO JSON structure ---
coco_json = {
    "info": {"description": "Dataset converted from Excel to COCO format", "contributor": "", "date_created": "2025-08-06T00:00:00Z"},
    "licenses": [{"id": 1, "name": "CC BY 4.0"}],
    "categories": [],
    "images": [],
    "annotations": []
}

# Populate the categories list in the JSON
for name, id_val in class_name_to_id.items():
    coco_json["categories"].append({"id": id_val, "name": name, "supercategory": "none"})

# Counters for unique image and annotation IDs
image_id_counter = 1
annotation_id_counter = 1
processed_images = {}

# --- Load data from Excel file ---
try:
    # Read the Excel file, ensuring the first column is treated as a string
    df = pd.read_excel(excel_file_path, header=None, dtype={0: str})
    image_base_names = df.iloc[:, 0].values
    x1 = df.iloc[:, 1].values
    y1 = df.iloc[:, 2].values
    x2 = df.iloc[:, 3].values
    y2 = df.iloc[:, 4].values
    classes_str = df.iloc[:, 5].values
except FileNotFoundError:
    print(f"Error: Excel file not found at '{excel_file_path}'")
    exit()
except Exception as e:
    print(f"Error reading Excel file: {e}")
    exit()

# --- FIX: Create a robust mapping of image numbers to file paths ---
# This is a new step that makes the code resilient to inconsistencies in the Excel data.
# It iterates through all the files in the image directory once and stores a dictionary
# mapping the numerical part (e.g., '1000') of the filename to its full path.
file_number_to_path = {}
for file_path in images_folder.glob('*'):
    if file_path.is_file():
        # Use regex to find the number inside parentheses, e.g., 'parandh (1000).JPG' -> '1000'
        match = re.search(r'\((\d+)\)', file_path.stem)
        if match:
            file_number = match.group(1)
            file_number_to_path[file_number] = file_path
        
# --- Process each entry and build the COCO JSON ---
for i in range(len(df)):
    try:
        # Get the filename or number from the Excel file
        excel_filename = str(image_base_names[i]).strip()

        if not excel_filename or pd.isna(excel_filename):
            print(f"Warning: Skipping empty or invalid image name at row {i+1}.")
            continue
        
        # Extract the number from the Excel value using regex.
        # This handles cases where the Excel value is 'parandh (1000).JPG' or just '1000'.
        match = re.search(r'\((\d+)\)', excel_filename)
        if not match:
            # Fallback for if the value is just a number string
            if excel_filename.isdigit():
                file_number = excel_filename
            else:
                print(f"Warning: Could not extract a number from filename '{excel_filename}' in row {i+1}. Skipping entry.")
                continue
        else:
            file_number = match.group(1)

        # Use the extracted number to find the corresponding image path from our map.
        # This is a much more reliable way to link the Excel data to the file on disk.
        image_path = file_number_to_path.get(file_number)
        
        if image_path is None:
            print(f"Warning: Image file not found for number '{file_number}' from row {i+1}. Skipping entry.")
            continue
        
        with Image.open(image_path) as img:
            image_width, image_height = img.size

        # Check if the image has already been processed to avoid duplicates
        if str(image_path) not in processed_images:
            image_id = image_id_counter
            image_entry = {
                "id": image_id,
                "file_name": image_path.name,
                "height": int(image_height),
                "width": int(image_width)
            }
            coco_json["images"].append(image_entry)
            processed_images[str(image_path)] = {"id": image_id}
            image_id_counter += 1
        else:
            image_id = processed_images[str(image_path)]["id"]

        # Process annotation data
        class_name = str(classes_str[i]).strip().lower() 
        class_id = class_name_to_id.get(class_name)

        if class_id is None:
            print(f"Error: Invalid class name '{classes_str[i]}' for image '{image_path.name}'. Skipping annotation.")
            continue

        x_min = float(x1[i])
        y_min = float(y1[i])
        bbox_width = float(x2[i] - x1[i])
        bbox_height = float(y2[i] - y1[i])
        area = bbox_width * bbox_height

        annotation_entry = {
            "id": annotation_id_counter,
            "image_id": image_id,
            "category_id": int(class_id),
            "bbox": [x_min, y_min, bbox_width, bbox_height],
            "area": area,
            "iscrowd": 0
        }
        coco_json["annotations"].append(annotation_entry)
        annotation_id_counter += 1

        print(f"✅ Processed entry {i+1}: Image '{image_path.name}' with class '{class_name}'")

    except Exception as e:
        image_name_for_error = image_base_names[i] if i < len(image_base_names) else f"row {i+1}"
        print(f"Error processing entry for '{image_name_for_error}': {e}")

# --- Save the final COCO JSON file ---
try:
    with open(output_json_file, "w", encoding='utf-8') as f:
        # Changed to indent=4 for better readability of the output JSON
        json.dump(coco_json, f, indent=4) 
    print(f"\n✅ Conversion complete! COCO JSON saved to {output_json_file}")
except Exception as e:
    print(f"Error saving the COCO JSON file: {e}")
