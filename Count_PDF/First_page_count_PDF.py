#pip install pymupdf tk
import unicodedata
import os
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

def normalize_persian_text(text):
    """Normalize Persian text for consistent character representation"""
    # Normalize to NFKC form for character standardization
    text = unicodedata.normalize('NFKC', text)
    # Replace similar Persian characters
    text = text.replace('ك', 'ک').replace('ي', 'ی').replace('ئ', 'ی')
    return text.strip().lower()

def select_folder():
    """Select folder containing PDF files"""
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select folder containing PDF files")
    return folder_path

def get_search_word():
    """Get search word from user"""
    root = tk.Tk()
    root.withdraw()
    word = simpledialog.askstring("Search Word", "Enter the word to search for:")
    return word

def search_first_page_with_normalization(folder_path, word):
    """Search for word in first page of PDFs with text normalization"""
    if not folder_path:
        messagebox.showerror("Error", "No folder selected!")
        return
    
    if not word:
        messagebox.showerror("Error", "No search word entered!")
        return
    
    # Normalize search word
    normalized_word = normalize_persian_text(word)
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
    count = 0

    result_text = ""
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        try:
            doc = fitz.open(pdf_path)
            if len(doc) > 0:
                # Extract text from first page
                text = doc[0].get_text()
                # Normalize extracted text
                normalized_text = normalize_persian_text(text)
                
                if normalized_word in normalized_text:
                    result_text += f"✓ Found in: {pdf_file}\n"
                    count += 1
                else:
                    result_text += f"✗ Not found in: {pdf_file}\n"
            doc.close()
        except Exception as e:
            result_text += f"⚠️ Error in {pdf_file}: {e}\n"

    # Show results in a window
    result_window = tk.Tk()
    result_window.title("Search Results")
    result_window.geometry("600x400")
    
    scrollbar = tk.Scrollbar(result_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    text_area = tk.Text(result_window, yscrollcommand=scrollbar.set)
    text_area.pack(fill=tk.BOTH, expand=True)
    
    # Results summary
    summary = "\n" + "="*50 + "\n"
    summary += f"📊 Files containing '{word}' on first page: {count} out of {len(pdf_files)}\n"
    
    text_area.insert(tk.END, result_text + summary)
    text_area.config(state=tk.DISABLED)
    scrollbar.config(command=text_area.yview)
    
    result_window.mainloop()

# Main program execution
if __name__ == "__main__":
    folder = select_folder()
    if folder:
        search_word = get_search_word()
        if search_word:
            search_first_page_with_normalization(folder, search_word)