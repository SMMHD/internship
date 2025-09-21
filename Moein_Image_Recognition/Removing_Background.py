import cv2
import os
import numpy as np
import matplotlib.pyplot as plt



def remove_background_from_logo(image_path, output_filename='logo_transparent.png'):
   
    # 1. خواندن تصویر
    img = cv2.imread(image_path)

    if img is None:
        print(f"خطا: فایل تصویر '{image_path}' پیدا نشد یا بارگذاری نشد.")
        return

    # 2. تعیین بازه رنگی پس‌زمینه (خاکستری تیره)
    # مقادیر BGR برای خاکستری تیره. اینها ممکن است نیاز به تنظیم دستی داشته باشند.
    # می‌توانید با استفاده از ابزارهایی مثل ColorZilla در مرورگر یا حتی Paint ویندوز،
    # رنگ پیکسلی از پس‌زمینه را پیدا کنید.
    # برای این تصویر (Rayan_Pajoohesh.jpg)، مقادیر BGR حدوداً (85, 85, 85) هستند.
    # ما یک بازه کوچک اطراف آن را در نظر می‌گیریم.
    lower_gray = np.array([60, 60, 60])
    upper_gray = np.array([253,255,254])

    # 3. ساخت ماسک
    # ماسک: پیکسل‌هایی که در بازه lower_gray تا upper_gray هستند (پس‌زمینه)، 255 می‌شوند. بقیه (متن)، 0 می‌شوند.
    mask = cv2.inRange(img, lower_gray, upper_gray)

    # 4. معکوس کردن ماسک:
    # ما ماسکی می‌خواهیم که متن (foreground) در آن سفید (255) و پس‌زمینه سیاه (0) باشد.
    # inRange() پس‌زمینه را 255 می‌کند، پس نیاز به معکوس کردن داریم.
    mask_inv = cv2.bitwise_not(mask)

    # 5. آماده سازی تصویر برای افزودن کانال آلفا (تبدیل به BGRA)
    # ابتدا کانال‌های BGR را جدا می‌کنیم
    b, g, r = cv2.split(img)
    
    # ماسک معکوس شده (که متن را نشان می‌دهد) را به عنوان کانال آلفا اضافه می‌کنیم
    # در اینجا، 255 در ماسک_inv یعنی مات و 0 یعنی شفاف.
    rgba = [b, g, r, mask_inv]
    transparent_image = cv2.merge(rgba)

    # 6. ذخیره تصویر با پس‌زمینه شفاف (فرمت PNG برای پشتیبانی از شفافیت)
    cv2.imwrite(output_filename, transparent_image)
    print(f"تصویر با پس‌زمینه شفاف با موفقیت در '{output_filename}' ذخیره شد.")

    #(اختیاری) نمایش تصاویر برای بررسی
    cv2.imshow('Original', img)
    cv2.imshow('Background Mask', mask) # ماسک اصلی (پس زمینه سفید)
    cv2.imshow('Inverted Mask (Foreground Mask)', mask_inv) # ماسک متن (متن سفید)
    cv2.imshow('Transparent Image Result', transparent_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# --- اجرای کد ---
# مطمئن شوید 'Rayan_Pajoohesh.jpg' در کنار فایل پایتون شما قرار دارد.
# یا مسیر کامل آن را بدهید: r'C:\Path\To\Rayan_Pajoohesh.jpg'
image_file = r'F:\University\6th term\Rayan_Pajoohesh.jpg'
output_file = r'F:\University\6th term\Rayan_Pajoohesh_transparent.png' # خروجی حتما باید PNG باشد!

remove_background_from_logo(image_file, output_file)

