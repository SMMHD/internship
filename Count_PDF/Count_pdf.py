#pip install pymupdf tk

import os
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog

def select_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_path = filedialog.askdirectory(title="Select folder containing PDF files")
    return folder_path

def count_pdfs_with_word(folder_path, word):
    if not folder_path:
        print("⚠️ No folder selected!")
        return
    
    word = word.strip().lower()  # Normalize for better matching
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
    count = 0

    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        try:
            doc = fitz.open(pdf_path)
            full_text = ""
            for page in doc:
                text = page.get_text().strip()
                if text:
                    full_text += text + "\n"
            doc.close()

            if word in full_text.lower():
                print(f"✓ Found in: {pdf_file}")
                count += 1
            else:
                print(f"✗ Not found in: {pdf_file}")

        except Exception as e:
            print(f"⚠️ Error in file {pdf_file}: {e}")

    print("\n----------------------------")
    print(f"📊 Number of files containing '{word}': {count} out of {len(pdf_files)}")

# === Usage ===
target_word = "ﮐﺸﺸﯽ"
folder_path = select_folder()
count_pdfs_with_word(folder_path, target_word)