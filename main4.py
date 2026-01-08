# lab2_image_basics.py
# المحتوى: قراءة الصور، المعلومات، الرسم، وتعديل البكسلات

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# سنقوم بإنشاء صورة وهمية (Dummy Image) للتجربة إذا لم تكن هناك صورة حقيقية
def create_dummy_image(path, width=400, height=400, color=(100, 150, 200)):
    # إنشاء مصفوفة ألوان عشوائية
    dummy = np.full((height, width, 3), color, dtype=np.uint8)
    cv2.imwrite(path, dummy)
    print(f"[Info] Created dummy image at {path}")

image_name = "sample.jpg"
create_dummy_image(image_name)

print("--- Part 1: Pillow (PIL) Basics ---")
# 1. قراءة صورة باستخدام Pillow
try:
    img_pil = Image.open(image_name)
    print(f"PIL Image Mode: {img_pil.mode}") # RGB, L, etc.
    print(f"PIL Image Size: {img_pil.size}") # (W, H)
    
    # 2. التعامل مع البكسل في Pillow
    pixel = img_pil.getpixel((0, 0)) # البكسل في الزاوية
    print(f"Pixel at (0,0): {pixel}")
    
    # تغيير لون بكسل معين
    img_pil.putpixel((50, 50), (255, 0, 0)) # لون أحمر
    # img_pil.show() # فتح نافذة لعرض الصورة (قد يعمل حسب النظام)
    img_pil.save("modified_pil.jpg")
    
except Exception as e:
    print(f"PIL Error: {e}")

print("\n--- Part 2: OpenCV Basics ---")
# 1. قراءة صورة باستخدام OpenCV
img_cv = cv2.imread(image_name)

if img_cv is not None:
    # OpenCV يستخدم BGR بشكل افتراضي
    print(f"OpenCV Shape (H, W, Channels): {img_cv.shape}")
    
    # 2. التعامل مع البكسل في OpenCV
    print(f"Pixel at (0,0): {img_cv[0, 0]}")
    img_cv[100, 100] = [0, 255, 0] # تغيير لون بكسل لأخضر (BGR)
    
    # 3. الرسم باستخدام OpenCV (Drawing)
    # رسم خط
    cv2.line(img_cv, (0, 0), (200, 200), (255, 0, 0), 5)
    # رسم مستطيل
    cv2.rectangle(img_cv, (50, 50), (150, 150), (0, 255, 0), 2)
    # رسم دائرة
    cv2.circle(img_cv, (300, 300), 50, (0, 0, 255), -1) # -1 يعني ملء
    
    cv2.imwrite("modified_cv.jpg", img_cv)
    print("[Done] OpenCV drawings saved.")
else:
    print("Failed to load image in OpenCV")

print("\n--- Part 3: Drawing with Pillow (Assignment 3) ---")
# رسم باستخدام Pillow
width, height = 400, 400
img_draw = Image.new('RGB', (width, height), color='white')
draw = ImageDraw.Draw(img_draw)

# رسم شكل بيضاوي
draw.ellipse([50, 50, 150, 150], fill='red', outline='black')
# رسم نص
try:
    # محاولة استخدام خط نظام، وإذا فشل استخدم الافتراضي
    font = ImageFont.truetype("arial.ttf", 24)
except IOError:
    font = ImageFont.load_default()

draw.text((50, 200), "Hello Pillow", fill='blue', font=font)

img_draw.save("pillow_drawing.jpg")
print("[Done] Pillow drawing saved.")

print("\n--- End of Lab 2 Basics ---")