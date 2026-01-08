import cv2 as cv
import numpy as np
import os
import matplotlib.pyplot as plt

# Linear Filtering: Mean and Gaussian Filters on Spatial Domain
path = "./src/images/noisysalterpepper.png"
if not os.path.exists(path):
    print(f"not Found {path}")
    # Creating a dummy image for demonstration if file not found
    image = np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8)
else:
    image = cv.imread(path)

# mean filter (row, col) should be odd numbers
image_mean = cv.blur(image, (5, 5))

# Gaussian filter (ksize should be odd numbers) and sigma value is standard deviation
image_gaussian = cv.GaussianBlur(image, (5, 5), 1)

plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))
plt.title('Original Image')

plt.subplot(1, 3, 2)
plt.imshow(cv.cvtColor(image_mean, cv.COLOR_BGR2RGB))
plt.title('Mean Filtered Image')

plt.subplot(1, 3, 3)
plt.imshow(cv.cvtColor(image_gaussian, cv.COLOR_BGR2RGB))
plt.title('Gaussian Filtered Image')

plt.show()
