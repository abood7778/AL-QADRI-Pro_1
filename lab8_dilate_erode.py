import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import os

path = './images/i.png'
if not os.path.exists(path):
    print(f"This Path {path} Not Found!!")
    # Creating a dummy image for demonstration if file not found
    image = np.zeros((300, 300, 3), dtype=np.uint8)
    cv.putText(image, 'I', (100, 200), cv.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 10)
else:
    image = cv.imread(path)

kernal = np.ones((5, 5), np.uint8)
dilation = cv.morphologyEx(image, cv.MORPH_DILATE, kernal)
erod = cv.morphologyEx(image, cv.MORPH_ERODE, kernal)
gradiant = cv.morphologyEx(image, cv.MORPH_GRADIENT, kernal)

plt.figure(figsize=(10, 10))
plt.subplot(1, 4, 1)
plt.title('Original Image')
plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))

plt.subplot(1, 4, 2)
plt.title('Dilation Image')
plt.imshow(cv.cvtColor(dilation, cv.COLOR_BGR2RGB))

plt.subplot(1, 4, 3)
plt.title('Eroded Image')
plt.imshow(cv.cvtColor(erod, cv.COLOR_BGR2RGB))

plt.subplot(1, 4, 4)
plt.title('Gradient Image')
plt.imshow(cv.cvtColor(gradiant, cv.COLOR_BGR2RGB))

plt.show()
