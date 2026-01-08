import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import os

path = './images/i_noise.png'
if not os.path.exists(path):
    print(f"This Path {path} Not Found!!")
    # Creating a dummy image for demonstration if file not found
    image = np.zeros((300, 300, 3), dtype=np.uint8)
    cv.putText(image, 'I', (100, 200), cv.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 10)
    # Add some noise
    noise = np.random.randint(0, 2, (300, 300, 3), dtype=np.uint8) * 255
    image = cv.bitwise_or(image, noise)
else:
    image = cv.imread(path)

kernal = np.ones((5, 5), np.uint8)
Open = cv.morphologyEx(image, cv.MORPH_OPEN, kernal)
TopHat = cv.morphologyEx(image, cv.MORPH_TOPHAT, kernal)

plt.figure(figsize=(10, 10))
plt.subplot(1, 3, 1)
plt.title('Original Image')
plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))

plt.subplot(1, 3, 2)
plt.title('Open Image')
plt.imshow(cv.cvtColor(Open, cv.COLOR_BGR2RGB))

plt.subplot(1, 3, 3)
plt.title('TopHat Image')
plt.imshow(cv.cvtColor(TopHat, cv.COLOR_BGR2RGB))

plt.show()
