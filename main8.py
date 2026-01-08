# lab_morphology_demo.py
# المحتوى: عرض جميع العمليات المورفولوجية

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os

# إنشاء صورة للتجربة
def create_test_image():
    image = np.zeros((300, 300, 3), dtype=np.uint8)
    cv.putText(image, 'TEST', (30, 200), cv.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 8)
    cv.rectangle(image, (50, 50), (100, 100), (255, 255, 255), -1)
    cv.circle(image, (200, 80), 30, (255, 255, 255), -1)
    return image

image = create_test_image()
kernel = np.ones((5, 5), np.uint8)

# العمليات المورفولوجية
dilation = cv.morphologyEx(image, cv.MORPH_DILATE, kernel)
erosion = cv.morphologyEx(image, cv.MORPH_ERODE, kernel)
opening = cv.morphologyEx(image, cv.MORPH_OPEN, kernel)
closing = cv.morphologyEx(image, cv.MORPH_CLOSE, kernel)
gradient = cv.morphologyEx(image, cv.MORPH_GRADIENT, kernel)
tophat = cv.morphologyEx(image, cv.MORPH_TOPHAT, kernel)
blackhat = cv.morphologyEx(image, cv.MORPH_BLACKHAT, kernel)

# عرض النتائج
titles = ['Original', 'Dilation', 'Erosion', 'Opening', 
          'Closing', 'Gradient', 'TopHat', 'BlackHat']
images = [image, dilation, erosion, opening, closing, gradient, tophat, blackhat]

plt.figure(figsize=(16, 8))
for i, (img, title) in enumerate(zip(images, titles)):
    plt.subplot(2, 4, i + 1)
    plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')

plt.tight_layout()
plt.savefig('morphology_results.png')
plt.show()

print("تم حفظ النتائج في morphology_results.png")
