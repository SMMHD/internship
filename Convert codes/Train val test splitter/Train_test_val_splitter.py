import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
import random

class YOLODatasetSplitter:
    def __init__(self, master):
        self.master = master
        master.title("YOLO Dataset Splitter")
        master.geometry("600x450")
        master.resizable(False, False)

        # Apply a modern look and feel using ttk
        style = ttk.Style()
        style.theme_use('clam')

        # Configure styles for labels, entries, and buttons
        style.configure('TLabel', font=('Inter', 10), padding=5)
        style.configure('TEntry', font=('Inter', 10), padding=5)
        # Temporarily comment out custom button styling to test
        # style.configure('TButton', font=('Inter', 10, 'bold'), padding=10, relief='raised', borderwidth=2)
        # style.map('TButton',
        #           foreground=[('active', 'white')],
        #           background=[('active', '#4CAF50')])

        # --- Input Paths Frame ---
        path_frame = ttk.LabelFrame(master, text="Input Paths", padding=(15, 10))
        path_frame.pack(padx=20, pady=10, fill="x", expand=True)

        # Image Folder
        ttk.Label(path_frame, text="Images Folder:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.images_path_entry = ttk.Entry(path_frame, width=50)
        self.images_path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(path_frame, text="Browse", command=self.browse_images_folder).grid(row=0, column=2, padx=5, pady=5)

        # Annotation Folder
        ttk.Label(path_frame, text="Annotations Folder:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.annotations_path_entry = ttk.Entry(path_frame, width=50)
        self.annotations_path_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(path_frame, text="Browse", command=self.browse_annotations_folder).grid(row=1, column=2, padx=5, pady=5)

        path_frame.grid_columnconfigure(1, weight=1)

        # --- Split Percentages Frame ---
        percentage_frame = ttk.LabelFrame(master, text="Split Percentages (%)", padding=(15, 10))
        percentage_frame.pack(padx=20, pady=10, fill="x", expand=True)

        # Train Percentage
        ttk.Label(percentage_frame, text="Train:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.train_percent_entry = ttk.Entry(percentage_frame, width=10)
        self.train_percent_entry.insert(0, "80")
        self.train_percent_entry.grid(row=0, column=1, padx=5, pady=5)

        # Validation Percentage
        ttk.Label(percentage_frame, text="Validation:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.val_percent_entry = ttk.Entry(percentage_frame, width=10)
        self.val_percent_entry.insert(0, "10")
        self.val_percent_entry.grid(row=0, column=3, padx=5, pady=5)

        # Test Percentage
        ttk.Label(percentage_frame, text="Test:").grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.test_percent_entry = ttk.Entry(percentage_frame, width=10)
        self.test_percent_entry.insert(0, "10")
        self.test_percent_entry.grid(row=0, column=5, padx=5, pady=5)

        # --- Output Folder Frame ---
        output_frame = ttk.LabelFrame(master, text="Output Folder", padding=(15, 10))
        output_frame.pack(padx=20, pady=10, fill="x", expand=True)

        ttk.Label(output_frame, text="Save to:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.output_path_entry = ttk.Entry(output_frame, width=50)
        self.output_path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(output_frame, text="Browse", command=self.browse_output_folder).grid(row=0, column=2, padx=5, pady=5)
        output_frame.grid_columnconfigure(1, weight=1)

        # --- Control Buttons ---
        button_frame = ttk.Frame(master, padding=(15, 10))
        button_frame.pack(pady=10)

        self.split_button = ttk.Button(button_frame, text="Split Dataset", command=self.split_dataset)
        self.split_button.pack(side="left", padx=10)

        self.exit_button = ttk.Button(button_frame, text="Exit", command=master.quit)
        self.exit_button.pack(side="right", padx=10)

        # --- Status Message ---
        self.status_label = ttk.Label(master, text="", foreground="blue", font=('Inter', 10, 'italic'))
        self.status_label.pack(pady=10)

    def browse_images_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.images_path_entry.delete(0, tk.END)
            self.images_path_entry.insert(0, folder_selected)

    def browse_annotations_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.annotations_path_entry.delete(0, tk.END)
            self.annotations_path_entry.insert(0, folder_selected)

    def browse_output_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.output_path_entry.delete(0, tk.END)
            self.output_path_entry.insert(0, folder_selected)

    def split_dataset(self):
        images_dir = self.images_path_entry.get()
        annotations_dir = self.annotations_path_entry.get()
        output_dir = self.output_path_entry.get()

        try:
            train_percent = float(self.train_percent_entry.get())
            val_percent = float(self.val_percent_entry.get())
            test_percent = float(self.test_percent_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for percentages.")
            return

        if not (0 <= train_percent <= 100 and 0 <= val_percent <= 100 and 0 <= test_percent <= 100):
            messagebox.showerror("Input Error", "Percentages must be between 0 and 100.")
            return

        if not (train_percent + val_percent + test_percent == 100):
            messagebox.showerror("Input Error", "Percentages must sum up to 100%.")
            return

        if not os.path.isdir(images_dir):
            messagebox.showerror("Path Error", "Images folder does not exist.")
            return
        if not os.path.isdir(annotations_dir):
            messagebox.showerror("Path Error", "Annotations folder does not exist.")
            return
        if not output_dir:
            messagebox.showerror("Path Error", "Please select an output folder.")
            return

        self.status_label.config(text="Processing...", foreground="orange")
        self.master.update_idletasks()

        try:
            image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'))]
            if not image_files:
                messagebox.showwarning("No Images Found", "No supported image files found in the specified images folder.")
                self.status_label.config(text="No images found.", foreground="red")
                return

            data_pairs = []
            for img_file in image_files:
                base_name = os.path.splitext(img_file)[0]
                annotation_file = base_name + '.txt'
                if os.path.exists(os.path.join(annotations_dir, annotation_file)):
                    data_pairs.append((img_file, annotation_file))
                else:
                    print(f"Warning: Annotation file for {img_file} not found. Skipping.")

            if not data_pairs:
                messagebox.showwarning("No Paired Data", "No image-annotation pairs found. Ensure image names match annotation names (e.g., image.jpg and image.txt).")
                self.status_label.config(text="No paired data found.", foreground="red")
                return

            random.shuffle(data_pairs)

            total_samples = len(data_pairs)
            num_train = int(total_samples * (train_percent / 100))
            num_val = int(total_samples * (val_percent / 100))
            num_test = total_samples - num_train - num_val

            train_data = data_pairs[:num_train]
            val_data = data_pairs[num_train : num_train + num_val]
            test_data = data_pairs[num_train + num_val :]

            output_base_dir = os.path.join(output_dir, "dataset_split")
            for folder_type in ["train", "val", "test"]:
                os.makedirs(os.path.join(output_base_dir, folder_type, "images"), exist_ok=True)
                os.makedirs(os.path.join(output_base_dir, folder_type, "labels"), exist_ok=True)

            def copy_files(data_list, target_type):
                for img_file, ann_file in data_list:
                    shutil.copy(os.path.join(images_dir, img_file), os.path.join(output_base_dir, target_type, "images", img_file))
                    shutil.copy(os.path.join(annotations_dir, ann_file), os.path.join(output_base_dir, target_type, "labels", ann_file))

            copy_files(train_data, "train")
            copy_files(val_data, "val")
            copy_files(test_data, "test")

            messagebox.showinfo("Success", f"Dataset split successfully!\n\n"
                                           f"Train samples: {len(train_data)}\n"
                                           f"Validation samples: {len(val_data)}\n"
                                           f"Test samples: {len(test_data)}\n\n"
                                           f"Output saved to: {output_base_dir}")
            self.status_label.config(text="Split complete!", foreground="green")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.status_label.config(text="Error during split.", foreground="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = YOLODatasetSplitter(root)
    root.mainloop()

