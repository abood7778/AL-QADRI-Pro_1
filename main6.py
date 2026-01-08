# lab3_image_ops.py
# المحتوى: Matplotlib، القنوات، القص، التكبير، الدوران

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# إنشاء صورة ملونة للتجربة
img_array = np.zeros((400, 400, 3), dtype=np.uint8)
img_array[50:350, 50:350] = [255, 100, 50] # مربع برتقالي
img_name = "lab3_img.jpg"
cv2.imwrite(img_name, img_array)

print("--- Part 1: Reading with Matplotlib ---")
# Matplotlib تقرأ الصور كـ RGB
img_plt = plt.imread(img_name)
print(f"Matplotlib Image Shape: {img_plt.shape}")

# عرض الصورة (اختياري)
# plt.imshow(img_plt)
# plt.axis('off')
# plt.show()

print("\n--- Part 2: Handling Color Channels ---")
# فصل القنوات في OpenCV
img_cv = cv2.imread(img_name)
b, g, r = cv2.split(img_cv)

# مثال: جعل الصورة زرقاء تماماً (إلغاء القناتين الحمراء والخضراء)
img_blue_only = img_cv.copy()
img_blue_only[:, :, 1] = 0 # Green = 0
img_blue_only[:, :, 2] = 0 # Red = 0
cv2.imwrite("blue_channel.jpg", img_blue_only)
print("[Done] Blue channel image saved.")

print("\n--- Part 3: Crop (Slicing) ---")
# قص جزء من الصورة (الإحداثيات: y1:y2, x1:x2)
# سنقص المربع البرتقالي من الصورة التي أنشأناها
crop_img = img_cv[50:350, 50:350]
cv2.imwrite("cropped_img.jpg", crop_img)
print(f"[Done] Image cropped. New shape: {crop_img.shape}")

print("\n--- Part 4: Resize & Rotate ---")
# 1. تكبير وتصغير (Resize)
# نريد أن نجعل الصورة 800x800
dim = (800, 800)
resized_img = cv2.resize(img_cv, dim, interpolation=cv2.INTER_AREA)
cv2.imwrite("resized_img.jpg", resized_img)

# 2. تدوير (Rotate)
# تدوير 90 درجة مع الساعة
rotated_90 = cv2.rotate(img_cv, cv2.ROTATE_90_CLOCKWISE)
cv2.imwrite("rotated_90.jpg", rotated_90)

# تدوير زاوية مخصصة (مثلاً 45 درجة) باستخدام مصفوفة الدوران
(h, w) = img_cv.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, 45, 1.0) # الزاوية 45، مقياس 1.0
rotated_45 = cv2.warpAffine(img_cv, M, (w, h))
cv2.imwrite("rotated_45.jpg", rotated_45)

print("[Done] Resized and Rotated images saved.")

print("\n--- End of Lab 3 Operations ---")