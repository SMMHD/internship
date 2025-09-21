import os
import glob
import json
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox

# --- The core conversion logic remains the same ---
def yolo_to_coco(yolo_dir, images_dir, output_dir):
    """
    Converts YOLOv5 annotations to COCO JSON format and saves the output
    as _annotations.coco.json in the specified output directory.
    """
    # Define class names based on the dataset
    class_names = ["eshpilkm", "keshpill", "neshpil", "eshpil"]
    
    # Construct the full output path with the predefined filename
    output_json = os.path.join(output_dir, "_annotations.coco.json")

    coco_json = {
        "info": {
            "year": "2025",
            "version": "1",
            "description": "Converted from YOLOv5 format",
            "contributor": "",
            "url": "",
            "date_created": "2025-08-06T00:00:00Z"
        },
        "licenses": [
            {"id": 1, "url": "https://creativecommons.org/licenses/by/4.0/", "name": "CC BY 4.0"}
        ],
        "categories": [],
        "images": [],
        "annotations": []
    }

    # Create categories
    for i, name in enumerate(class_names):
        coco_json["categories"].append({"id": i, "name": name, "supercategory": "none"})

    annotation_id = 1
    image_id = 1
    
    yolo_files = glob.glob(os.path.join(yolo_dir, "*.txt"))
    if not yolo_files:
        messagebox.showerror("Error", f"No .txt annotation files found in {yolo_dir}.")
        return

    for yolo_file in yolo_files:
        try:
            image_filename_base_from_yolo = os.path.basename(yolo_file).replace(".txt", "")
            image_path = None
            image_filename = None
            original_image_name_extra = None

            for ext in [".jpg", ".jpeg", ".png", ".bmp"]:
                temp_path = os.path.join(images_dir, image_filename_base_from_yolo + ext)
                if os.path.exists(temp_path):
                    image_path = temp_path
                    image_filename = image_filename_base_from_yolo + ext
                    
                    if ".rf." in image_filename:
                        parts = image_filename.split(".rf.")
                        if len(parts) > 1:
                            original_base_with_ext = parts[0]
                            if '_jpg' in original_base_with_ext:
                                original_image_name_extra = original_base_with_ext.replace('_jpg', '') + '.jpg'
                            elif '_png' in original_base_with_ext:
                                original_image_name_extra = original_base_with_ext.replace('_png', '') + '.png'
                            else:
                                original_image_name_extra = parts[0] + os.path.splitext(image_filename)[1]
                        else:
                            original_image_name_extra = image_filename
                    else:
                        original_image_name_extra = image_filename
                    break

            if not image_path:
                continue

            with Image.open(image_path) as img:
                image_width, image_height = img.size

            image_entry = {
                "id": image_id,
                "license": 1,
                "file_name": image_filename,
                "height": image_height,
                "width": image_width,
                "date_captured": "2025-04-28T17:32:29+00:00"
            }
            if original_image_name_extra:
                image_entry["extra"] = {"name": original_image_name_extra}
            
            coco_json["images"].append(image_entry)

            with open(yolo_file, "r") as f:
                for line in f.readlines():
                    parts = line.strip().split()
                    if len(parts) == 5:
                        class_id, x_center, y_center, bbox_width, bbox_height = map(float, parts)
                        x_min = x_center * image_width - (bbox_width * image_width / 2)
                        y_min = y_center * image_height - (bbox_height * image_height / 2)
                        bbox_width_abs = bbox_width * image_width
                        bbox_height_abs = bbox_height * image_height
                        
                        coco_json["annotations"].append({
                            "id": annotation_id,
                            "image_id": image_id,
                            "category_id": int(class_id),
                            "bbox": [x_min, y_min, bbox_width_abs, bbox_height_abs],
                            "area": bbox_width_abs * bbox_height_abs,
                            "iscrowd": 0
                        })
                        annotation_id += 1
            
            image_id += 1
        except Exception as e:
            messagebox.showwarning("Warning", f"An error occurred while processing {yolo_file}: {e}. Skipping.")
            continue

    try:
        with open(output_json, "w") as f:
            json.dump(coco_json, f)
        messagebox.showinfo("Success", f"✅ Conversion complete. COCO JSON saved to {output_json}")
    except PermissionError:
        messagebox.showerror("Error", f"❌ Permission denied. Make sure you have write permissions for the directory: {os.path.dirname(output_json)}")
    except Exception as e:
        messagebox.showerror("Error", f"❌ An error occurred while saving the JSON file: {e}")

# --- GUI implementation ---
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YOLO to COCO Converter")
        self.geometry("600x200")
        self.yolo_dir = tk.StringVar()
        self.images_dir = tk.StringVar()
        self.output_dir = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Frame for YOLO directory
        frame1 = tk.Frame(self)
        frame1.pack(fill='x', padx=10, pady=5)
        tk.Label(frame1, text="YOLO Annotations Directory:", width=25, anchor='w').pack(side='left')
        tk.Entry(frame1, textvariable=self.yolo_dir, state='readonly').pack(side='left', expand=True, fill='x', padx=5)
        tk.Button(frame1, text="Browse", command=self.browse_yolo_dir).pack(side='right')

        # Frame for Images directory
        frame2 = tk.Frame(self)
        frame2.pack(fill='x', padx=10, pady=5)
        tk.Label(frame2, text="Images Directory:", width=25, anchor='w').pack(side='left')
        tk.Entry(frame2, textvariable=self.images_dir, state='readonly').pack(side='left', expand=True, fill='x', padx=5)
        tk.Button(frame2, text="Browse", command=self.browse_images_dir).pack(side='right')
        
        # Frame for Output Directory
        frame3 = tk.Frame(self)
        frame3.pack(fill='x', padx=10, pady=5)
        tk.Label(frame3, text="Output Directory:", width=25, anchor='w').pack(side='left')
        tk.Entry(frame3, textvariable=self.output_dir, state='readonly').pack(side='left', expand=True, fill='x', padx=5)
        tk.Button(frame3, text="Browse", command=self.browse_output_dir).pack(side='right')

        # Conversion button
        convert_button = tk.Button(self, text="Start Conversion", command=self.run_conversion)
        convert_button.pack(pady=20, ipadx=20, ipady=10)

    def browse_yolo_dir(self):
        directory = filedialog.askdirectory(title="Select YOLO Labels Directory")
        if directory:
            self.yolo_dir.set(directory)

    def browse_images_dir(self):
        directory = filedialog.askdirectory(title="Select Images Directory")
        if directory:
            self.images_dir.set(directory)
            
    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir.set(directory)
    
    def run_conversion(self):
        yolo_dir_path = self.yolo_dir.get()
        images_dir_path = self.images_dir.get()
        output_dir_path = self.output_dir.get()

        if not all([yolo_dir_path, images_dir_path, output_dir_path]):
            messagebox.showwarning("Incomplete Information", "Please select all three directories before converting.")
            return

        yolo_to_coco(yolo_dir_path, images_dir_path, output_dir_path)

if __name__ == "__main__":
    app = App()
    app.mainloop()