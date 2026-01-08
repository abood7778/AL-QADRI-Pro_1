from PIL import Image
import os

image_path = "./images/game.jpg"

output_dir = "output_images_topic9"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

if not os.path.exists(image_path):
    print(f"الصورة غير موجودة: {image_path}")
else:
    try:
        with Image.open(image_path) as img:
            if img.mode != "RGB":
                img = img.convert('RGB')
            qualities = [95, 75, 50, 25, 10]
            print("\nحفظ الصورة بجودات مختلفة JPEG")
            for q in qualities:
                output_path = os.path.join(output_dir, f"image_q{q}.jpg")
                img.save(output_path, quality=q)
                file_size = os.path.getsize(output_path)
                print(f"تم حفظ الملف {output_path} (الجودة {q}, الحجم {file_size / 1024:.2f} KB)")
            original_file_size = os.path.getsize(image_path)
            print(f"\nالحجم الأصلي ({image_path}): {original_file_size / 1024:.2f} KB")
    except Exception as e:
        print(f"حدث خطأ: {e}")

