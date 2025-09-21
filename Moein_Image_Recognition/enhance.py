import cv2
import numpy as np
import os
from matplotlib import pyplot as plt

# مسیر پوشه
folder_path = r"C:\Users\dehmi\Downloads\images"
files = os.listdir(folder_path)
image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# ایجاد CLAHE
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

for filename in image_files:
    img_path = os.path.join(folder_path, filename)
    img_bgr = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # ======= پردازش RGB روی هر سه کانال
    r, g, b = cv2.split(img_rgb)
    img_eq_rgb = cv2.merge([
        cv2.equalizeHist(r), cv2.equalizeHist(g), cv2.equalizeHist(b)
    ])
    img_clahe_rgb = cv2.merge([
        clahe.apply(r), clahe.apply(g), clahe.apply(b)
    ])

    # ======= پردازش HSV روی V
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(img_hsv)
    v_eq = cv2.equalizeHist(v)
    v_clahe = clahe.apply(v)
    img_hsv_eq = cv2.merge([h, s, v_eq])
    img_hsv_clahe = cv2.merge([h, s, v_clahe])
    img_hsv_eq_rgb = cv2.cvtColor(img_hsv_eq, cv2.COLOR_HSV2RGB)
    img_hsv_clahe_rgb = cv2.cvtColor(img_hsv_clahe, cv2.COLOR_HSV2RGB)

    # ======= پردازش YCrCb روی Y
    img_ycrcb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(img_ycrcb)
    y_eq = cv2.equalizeHist(y)
    y_clahe = clahe.apply(y)
    img_ycrcb_eq = cv2.merge([y_eq, cr, cb])
    img_ycrcb_clahe = cv2.merge([y_clahe, cr, cb])
    img_ycrcb_eq_rgb = cv2.cvtColor(img_ycrcb_eq, cv2.COLOR_YCrCb2RGB)
    img_ycrcb_clahe_rgb = cv2.cvtColor(img_ycrcb_clahe, cv2.COLOR_YCrCb2RGB)

    # ======= پردازش LAB روی L
    img_lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(img_lab)
    l_eq = cv2.equalizeHist(l)
    l_clahe = clahe.apply(l)
    img_lab_eq = cv2.merge([l_eq, a, b])
    img_lab_clahe = cv2.merge([l_clahe, a, b])
    img_lab_eq_rgb = cv2.cvtColor(img_lab_eq, cv2.COLOR_LAB2RGB)
    img_lab_clahe_rgb = cv2.cvtColor(img_lab_clahe, cv2.COLOR_LAB2RGB)

    # ======= نمایش نتایج
    plt.figure(figsize=(18,12))
    plt.suptitle(f"Processing: {filename}", fontsize=16)

    titles = [
        "Original",
        "RGB Equalized", "RGB CLAHE",
        "HSV Equalized (V)", "HSV CLAHE (V)",
        "YCrCb Equalized (Y)", "YCrCb CLAHE (Y)",
        "LAB Equalized (L)", "LAB CLAHE (L)"
    ]
    images = [
        img_rgb,
        img_eq_rgb, img_clahe_rgb,
        img_hsv_eq_rgb, img_hsv_clahe_rgb,
        img_ycrcb_eq_rgb, img_ycrcb_clahe_rgb,
        img_lab_eq_rgb, img_lab_clahe_rgb
    ]

    for i, (title, img) in enumerate(zip(titles, images)):
        plt.subplot(3, 3, i+1)
        plt.imshow(img)
        plt.title(title, fontsize=10)
        plt.axis('off')

    plt.tight_layout()
    plt.show()
