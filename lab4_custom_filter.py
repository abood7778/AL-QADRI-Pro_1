import cv2 as cv
import numpy as np
import os
import matplotlib.pyplot as plt

# Custom Linear Filtering using filter2D
path = "./src/images/noisysalterpepper.png"
if not os.path.exists(path):
    print(f"not Found {path}")
    # Creating a dummy image for demonstration if file not found
    image = np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8)
else:
    image = cv.imread(path)

ones_mask = np.ones((5, 5), np.float32) / 25
mask = np.array([[1, 1, 1],
                 [1, 1, 1],
                 [1, 1, 1]], np.float32) / 9

image_filter2d = cv.filter2D(image, -1, mask)
image_filter2d_ones = cv.filter2D(image, -1, ones_mask)

plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))
plt.title('Original Image')

plt.subplot(1, 3, 2)
plt.imshow(cv.cvtColor(image_filter2d, cv.COLOR_BGR2RGB))
plt.title('Custom Filtered Image (3x3)')

plt.subplot(1, 3, 3)
plt.imshow(cv.cvtColor(image_filter2d_ones, cv.COLOR_BGR2RGB))
plt.title('Custom Filtered Image (5x5)')

plt.show()
