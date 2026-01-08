# lab3_assignments.py
# المحتوى: برنامج تفاعلي للتعديل، ودمج صور (منتج + خلفية)

import cv2
import numpy as np
from PIL import Image

print("--- Assignment 1: Interactive Image Editor ---")
# سنستخدم صورة وهمية لعدم وجود صورة لدى المستخدم
img_name = "edit_sample.jpg"
cv2.imwrite(img_name, np.zeros((400, 400, 3), dtype=np.uint8))

def edit_image_menu():
    print("\n1. Crop")
    print("2. Resize")
    print("3. Rotate")
    print("4. Exit")
    choice = input("Enter choice (1-4): ")
    
    if choice == '1':
        try:
            y = int(input("Enter Y start: "))
            x = int(input("Enter X start: "))
            h = int(input("Enter Height: "))
            w = int(input("Enter Width: "))
            img = cv2.imread(img_name)
            cropped = img[y:y+h, x:x+w]
            cv2.imwrite("edited_result.jpg", cropped)
            print("Image Cropped and saved as 'edited_result.jpg'")
        except:
            print("Invalid coordinates or image error.")
            
    elif choice == '2':
        try:
            w = int(input("Enter new Width: "))
            h = int(input("Enter new Height: "))
            img = cv2.imread(img_name)
            resized = cv2.resize(img, (w, h))
            cv2.imwrite("edited_result.jpg", resized)
            print("Image Resized and saved.")
        except:
            print("Invalid size.")
            
    elif choice == '3':
        try:
            angle = float(input("Enter Angle: "))
            img = cv2.imread(img_name)
            (h, w) = img.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(img, M, (w, h))
            cv2.imwrite("edited_result.jpg", rotated)
            print("Image Rotated and saved.")
        except:
            print("Error rotating.")
            
    elif choice == '4':
        return False
    return True

# تشغيل القائمة (للتجربة)
# while edit_image_menu():
#     pass

print("\n--- Assignment 3: Merge Product & Background (Pillow) ---")
# سنقوم بإنشاء صور وهمية للمحاكاة

# 1. إنشاء خلفية (Background)
bg = Image.new('RGB', (800, 600), color='skyblue')
bg.save("background.jpg")

# 2. إنشاء منتج بدون خلفية (Product with transparency - RGBA)
# صورة دائرة تمثل المنتج
product = Image.new('RGBA', (200, 200), (0, 0, 0, 0)) # شفاف
from PIL import ImageDraw
draw = ImageDraw.Draw(product)
draw.ellipse([0, 0, 200, 200], fill='red', outline='white')
product.save("product.png")

# كود الدمج
try:
    background = Image.open("background.jpg").convert("RGBA")
    product = Image.open("product.png").convert("RGBA")
    
    # تغيير حجم المنتج ليكون مناسب
    product = product.resize((150, 150))
    
    # تحديد موقع المنتج على الخلفية (مثلاً في المنتصف)
    position = (background.width // 2 - 75, background.height // 2 - 75)
    
    # الدمج باستخدام alpha channel (الشفافية)
    background.paste(product, position, product) # المعلمة الثالثة هي mask للشفافية
    
    # حفظ الصورة النهائية
    background.convert("RGB").save("final_merged.jpg")
    print("[Done] Product merged with background saved as 'final_merged.jpg'")
    
except Exception as e:
    print(f"Error merging images: {e}")

print("\n--- End of Lab 3 Assignments ---")