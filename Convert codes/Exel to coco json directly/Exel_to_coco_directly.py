import pandas as pd
from PIL import Image
import os
import json
from pathlib import Path

# --- Configuration ---
# Update these paths to match your folder structure
excel_file_path = Path(r"H:\Hosseini\dataset\xlx\tt.xlsx")
images_folder = Path(r"H:\Hosseini\dataset\Compressed images")
output_json_file = Path(r"H:\Hosseini\dataset\annotations.coco.json")

# Define class names and their corresponding IDs.
# This must match the classes in your Excel file.
class_name_to_id = {
    'eshpil': 0,
    'keshpli': 1,
    'neshpil': 2,
    'eshpilkm': 3,
}

# --- Initialize COCO JSON structure ---
coco_json = {
    "info": {
        "description": "Dataset converted from Excel to COCO format",
        "contributor": "",
        "date_created": "2025-08-06T00:00:00Z"
    },
    "licenses": [
        {
            "id": 1,
            "name": "CC BY 4.0"
        }
    ],
    "categories": [],
    "images": [],
    "annotations": []
}

# Create categories based on the class_name_to_id dictionary
for name, id in class_name_to_id.items():
    coco_json["categories"].append({
        "id": id,
        "name": name,
        "supercategory": "none"
    })

# Initialize counters and dictionaries for efficient processing
image_id_counter = 1
annotation_id_counter = 1
processed_images = {} # To avoid adding duplicate image entries

# --- Load data from Excel file ---
try:
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

# --- Process each entry and build the COCO JSON ---
for i in range(len(x1)):
    try:
        image_base_name = image_base_names[i]

        # Determine the correct image path by checking for various extensions
        image_path = None
        for ext in ['', '.jpg', '.jpeg', '.JPG', '.JPEG']:
            temp_path = images_folder / f"{image_base_name}{ext}"
            if temp_path.is_file():
                image_path = temp_path
                break
        
        if image_path is None:
            print(f"Warning: Image file not found for '{image_base_name}'. Skipping entry {i}.")
            continue
        
        # Open image to get dimensions
        with Image.open(image_path) as img:
            image_width, image_height = img.size

        # Check if the image has already been added to the COCO JSON
        if str(image_path) not in processed_images:
            # Add new image entry
            image_entry = {
                "id": image_id_counter,
                "file_name": image_path.name,
                # Explicitly cast to Python int to avoid JSON serialization errors
                "height": int(image_height),
                "width": int(image_width)
            }
            coco_json["images"].append(image_entry)
            
            # Store image info for future annotations
            processed_images[str(image_path)] = {
                "id": image_id_counter,
                "width": int(image_width),
                "height": int(image_height)
            }
            image_id = image_id_counter
            image_id_counter += 1
        else:
            # Use the existing image ID
            image_info = processed_images[str(image_path)]
            image_id = image_info["id"]

        # Normalize the class name and get its ID
        class_name = str(classes_str[i]).strip().lower() 
        class_id = class_name_to_id.get(class_name)

        if class_id is None:
            print(f"Error: Invalid class name '{classes_str[i]}' for image '{image_base_names[i]}'. Skipping this entry.")
            continue

        # Convert coordinates to COCO format (x_min, y_min, bbox_width_abs, bbox_height_abs)
        # Coordinates are from the Excel file. Explicitly cast to Python float.
        x_min = float(x1[i])
        y_min = float(y1[i])
        bbox_width = float(x2[i] - x1[i])
        bbox_height = float(y2[i] - y1[i])
        
        # Calculate area
        area = bbox_width * bbox_height

        # Create annotation entry
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

        print(f"✅ Processed entry {i}: Image '{image_path.name}' with class '{class_name}'")

    except Exception as e:
        print(f"Error processing entry {i} (Image: {image_base_names[i]}): {e}")

# --- Save the final COCO JSON file ---
try:
    with open(output_json_file, "w") as f:
        # Using separators=(',', ':') to minify the JSON output
        json.dump(coco_json, f, separators=(',', ':'))
    print(f"\n✅ Conversion complete! Minified COCO JSON saved to {output_json_file}")
except Exception as e:
    print(f"Error saving the COCO JSON file: {e}")
