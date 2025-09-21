
#pip install pymupdf tk
import unicodedata
import os
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, simpledialog

def normalize_persian_text(text):
    """نرمال‌سازی متن پارسی برای یکسان‌سازی نمایش حروف."""
    # نرمال‌سازی به فرم NFKC برای استانداردسازی حروف
    text = unicodedata.normalize('NFKC', text)
    # جایگزینی حروف پارسی مشابه
    text = text.replace('ك', 'ک').replace('ي', 'ی').replace('ئ', 'ی')
    return text.strip().lower()

def select_folder():
    root = tk.Tk()
    root.withdraw()  # مخفی کردن پنجره اصلی
    folder_path = filedialog.askdirectory(title="Select folder containing PDF files")
    return folder_path

def get_search_word():
    root = tk.Tk()
    root.withdraw()  # مخفی کردن پنجره اصلی
    word = simpledialog.askstring("Input", "Enter the word to search for:", parent=root)
    return word

def count_pdfs_with_word(folder_path, word):
    if not folder_path:
        print("⚠️ No folder selected!")
        return
    
    if not word:
        print("⚠️ No search word entered!")
        return
    
    # نرمال‌سازی کلمه جست‌وجو
    normalized_word = normalize_persian_text(word)
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

            # نرمال‌سازی متن PDF
            normalized_text = normalize_persian_text(full_text)
            
            if normalized_word in normalized_text:
                print(f"✓ Found in: {pdf_file}")
                count += 1
            else:
                print(f"✗ Not found in: {pdf_file}")

        except Exception as e:
            print(f"⚠️ Error in file {pdf_file}: {e}")

    print("\n----------------------------")
    print(f"📊 Number of files containing '{word}': {count} out of {len(pdf_files)}")

# === استفاده ===
folder_path = select_folder()
if folder_path:  # فقط اگه پوشه انتخاب شد، پنجره ورودی کلمه باز بشه
    target_word = get_search_word()
    count_pdfs_with_word(folder_path, target_word)