import os
import numpy as np
import torch
import torchvision.transforms as T
from PIL import Image
from rfdetr import RFDETRMedium
import torch.nn.functional as F
import supervision as sv

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = RFDETRMedium(
    pretrain_weights="/home/vira/rf-dter/rf-detr-develop/rfdetr/output/train 4/checkpoint_best_total.pth",
    image_size=1024,
    patch_size=16,
    num_classes=3
)

torch_model = model.model.model
torch_model.eval()
torch_model.to(device)

# این بخش transform را به گونه‌ای تنظیم کنید که فقط نرمال‌سازی را انجام دهد
transform = T.Compose([
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

input_folder = "/home/vira/rf-dter/dataset/test"
output_folder = "/home/vira/rf-dter/dataset/test/annotated"
os.makedirs(output_folder, exist_ok=True)

threshold = 0.9

for filename in os.listdir(input_folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        print(f"در حال پردازش: {filename}")
        image_path = os.path.join(input_folder, filename)
        
        # 1. تصویر را باز کنید
        image = Image.open(image_path).convert("RGB")
        
        # 2. رزولوشن اصلی تصویر را بخوانید و ذخیره کنید
        original_w, original_h = image.size

        # 3. تصویر را به اندازه ورودی مدل (1024x1024) تغییر دهید
        resized_image = image.resize((1024, 1024))
        input_tensor = transform(resized_image).unsqueeze(0).to(device)

        with torch.no_grad():
            outputs = torch_model(input_tensor)

        pred_logits = outputs["pred_logits"]
        pred_boxes = outputs["pred_boxes"]

        probs = F.softmax(pred_logits[0], dim=-1)
        probs_no_bg = probs[:, :-1]
        scores, labels = probs_no_bg.max(dim=-1)

        keep = scores > threshold

        boxes = pred_boxes[0][keep].cpu()
        labels = labels[keep].cpu()
        scores = scores[keep].cpu()

        if len(boxes) == 0:
            print(f"هیچ شیئی برای تصویر {filename} تشخیص داده نشد، رد می‌شود.")
            continue

        boxes_cxcywh = boxes.numpy()
        boxes_xyxy = []

        # 4. جعبه‌های مرزی را با توجه به ابعاد اصلی تصویر مقیاس‌بندی کنید
        for cx, cy, w, h in boxes_cxcywh:
            x1 = (cx - w / 2) * original_w
            y1 = (cy - h / 2) * original_h
            x2 = (cx + w / 2) * original_w
            y2 = (cy + h / 2) * original_h
            boxes_xyxy.append([x1, y1, x2, y2])

        boxes_xyxy_np = np.array(boxes_xyxy)

        detections = sv.Detections(
            xyxy=boxes_xyxy_np,
            confidence=scores.numpy(),
            class_id=labels.numpy()
        )

        if hasattr(model.model, "class_labels"):
            class_names = model.model.class_labels
        else:
            class_names = {0: "keshpil", 1: "eshpil", 2: "nehpil"}

        label_names = [class_names.get(id, str(id)) for id in labels.numpy()]

        box_annotator = sv.BoxAnnotator(color=sv.ColorPalette.DEFAULT)
        label_annotator = sv.LabelAnnotator(color=sv.ColorPalette.DEFAULT)

        annotated_image = box_annotator.annotate(image.copy(), detections)
        annotated_image = label_annotator.annotate(annotated_image, detections, labels=label_names)

        output_path = os.path.join(output_folder, filename)
        annotated_image.save(output_path)
        print(f"فایل ذخیره شد: {output_path}")
