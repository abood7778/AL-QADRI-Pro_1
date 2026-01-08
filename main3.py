# lab1_text_files.py
# المحتوى: أساسيات النصوص، الترميز، والتعامل مع الملفات (File I/O)

print("--- Part 1: Text Encoding & Strings ---")

# 1. تعريف نص وتجربة العمليات الأساسية
text = "Hello World"
print(f"Original Text: {text}")

# تحويل الحالة (Upper, Lower)
print(f"Upper: {text.upper()}")
print(f"Lower: {text.lower()}")

# البحث والاستبدال
if "World" in text:
    print("'World' exists in text.")
    
new_text = text.replace("World", "Python")
print(f"After Replace: {new_text}")

# التقسيم والدمج
words = text.split()
print(f"Split: {words}")
joined_text = "-".join(words)
print(f"Joined: {joined_text}")

print("\n--- Part 2: File Handling (I/O) ---")

# اسم الملف الذي سنعمل عليه
filename = "lab_data.txt"

# 1. كتابة في ملف (Write Mode 'w')
# ملاحظة: الوضع 'w' يمسح المحتوى السابق إذا كان الملف موجوداً
try:
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Name: Malek A.Almosanif\n")
        f.write("Course: Multimedia IT3\n")
        f.write("Topic: Python Basics\n")
    print(f"[Done] Data written to {filename}")
except Exception as e:
    print(f"Error writing file: {e}")

# 2. قراءة من ملف (Read Mode 'r')
try:
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
        print("\n--- File Content (Read All) ---")
        print(content)
except FileNotFoundError:
    print("File not found.")

# 3. إضافة محتوى لنهاية الملف (Append Mode 'a')
try:
    with open(filename, "a", encoding="utf-8") as f:
        f.write("New Line Added via Append Mode.\n")
    print("[Done] New line appended.")
except Exception as e:
    print(f"Error appending file: {e}")

# 4. قراءة سطر بسطر
print("\n--- Reading Line by Line ---")
try:
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            print(f"Line: {line.strip()}")
except Exception as e:
    print(e)

print("\n--- End of Lab 1 ---")