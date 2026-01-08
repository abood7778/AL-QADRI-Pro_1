# lab2_assignments.py
# المحتوى: واجبات لاب 2 (رسم SVG، تحويل صيغ الصور)

import os
from PIL import Image

print("--- Assignment 1: Draw SVG Logo ---")
# إنشاء ملف SVG
svg_content = """<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
  <circle cx="100" cy="100" r="80" stroke="green" stroke-width="4" fill="yellow" />
  <text x="50%" y="50%" font-family="Arial" font-size="20" fill="black" text-anchor="middle" dy=".3em">My Logo</text>
</svg>"""

with open("logo.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)
print("[Done] logo.svg created.")

print("\n--- Assignment 2: Pillow vs OpenCV Comparison ---")
comparison = """
Comparison:
- Pillow (PIL): مكتوبة بلغة بايثون، ممتازة للعمليات الأساسية.
- OpenCV: مكتوبة بـ C/C++، أسرع في معالجة الفيديو ورؤية الكمبيوتر.
- Use Pillow for: تحرير الصور البسيطة، الدمج.
- Use OpenCV for: معالجة متقدمة، اكتشاف الوجوه.
"""
print(comparison)

print("\n--- Assignment 4: Batch Image Convert (Folder to JPG) ---")
# إنشاء مجلد للتجربة
os.makedirs("images_folder", exist_ok=True)
for i in range(3):
    img = Image.new('RGB', (100, 100), color=(i * 80, 100, 150))
    img.save(f"images_folder/img_{i}.png")

folder_path = "images_folder"
output_path = "converted_images"
os.makedirs(output_path, exist_ok=True)

files = os.listdir(folder_path)
for filename in files:
    if filename.endswith((".png", ".bmp")):
        try:
            img_path = os.path.join(folder_path, filename)
            img = Image.open(img_path)
            
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
                
            new_name = os.path.splitext(filename)[0] + ".jpg"
            save_path = os.path.join(output_path, new_name)
            img.save(save_path)
            print(f"[Converted] {filename} -> {new_name}")
        except Exception as e:
            print(f"Error converting {filename}: {e}")

print("\n--- End of Lab 2 Assignments ---")