import cv2
import numpy as np
import matplotlib.pyplot as plt # برای نمایش هیستوگرام‌ها

def analyze_and_plot_histogram(image_path):
    """
    تصویر را می‌خواند، هیستوگرام‌های خاکستری و رنگی آن را محاسبه و نمایش می‌دهد.
    """
    # 1. خواندن تصویر
    img = cv2.imread(image_path)

    if img is None:
        print(f"خطا: فایل تصویر '{image_path}' پیدا نشد یا بارگذاری نشد.")
        return

    # --- هیستوگرام تصویر خاکستری ---
    print("\n--- محاسبه هیستوگرام برای تصویر خاکستری ---")
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # محاسبه هیستوگرام برای تصویر خاکستری
    # [gray_img]: تصویر ورودی در یک لیست
    # [0]: فقط کانال 0 (تنها کانال تصویر خاکستری)
    # None: بدون ماسک (یعنی کل تصویر)
    # [256]: 256 خانه برای مقادیر 0 تا 255
    # [0, 256]: بازه مقادیر پیکسلی
    hist_gray = cv2.calcHist([gray_img], [0], None, [256], [0, 256])

    # نمایش هیستوگرام خاکستری با Matplotlib
    plt.figure(figsize=(8, 6))
    plt.title("Histogram for Grayscale Image")
    plt.xlabel("Pixel Intensity")
    plt.ylabel("Number of Pixels")
    plt.plot(hist_gray, color='black') # رسم هیستوگرام به رنگ سیاه
    plt.xlim([0, 256]) # محدودیت محور X از 0 تا 255
    plt.grid(True, linestyle='--', alpha=0.6) # اضافه کردن خطوط شبکه
    plt.show()


    # --- هیستوگرام برای تصاویر رنگی (BGR) ---
    print("\n--- محاسبه هیستوگرام برای کانال‌های رنگی (BGR) ---")
    colors = ('b', 'g', 'r') # نام کانال‌ها برای Matplotlib (Blue, Green, Red)
    
    plt.figure(figsize=(10, 6))
    plt.title("Histogram for Color Image Channels (BGR)")
    plt.xlabel("Pixel Intensity")
    plt.ylabel("Number of Pixels")

    for i, col in enumerate(colors):
        # محاسبه هیستوگرام برای هر کانال جداگانه
        # [img]: تصویر ورودی
        # [i]: اندیس کانال فعلی (0 برای B، 1 برای G، 2 برای R)
        hist_channel = cv2.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(hist_channel, color=col) # رسم هیستوگرام با رنگ کانال مربوطه
        plt.xlim([0, 256])

    plt.legend(['Blue Channel', 'Green Channel', 'Red Channel']) # اضافه کردن راهنما
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()

    print("تحلیل هیستوگرام به پایان رسید.")

# --- اجرای کد ---
# مطمئن شوید که فایل 'your_image.jpg' (یا هر فرمت دیگری) در کنار فایل پایتون شما قرار دارد.
# یا مسیر کامل آن را بدهید: r'C:\Path\To\Your\your_image.jpg'
image_to_analyze = r'F:\University\6th term\Bite_Bitters_2.jpg' # نام فایل تصویر خود را اینجا قرار دهید

analyze_and_plot_histogram(image_to_analyze)