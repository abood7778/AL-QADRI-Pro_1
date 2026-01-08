import cv2 as cv
import numpy as np
import os
import matplotlib.pyplot as plt

# Non-Linear Filtering: Median Filter on Spatial Domain
path = "./src/images/noisysalterpepper.png"
if not os.path.exists(path):
    print(f"not Found {path}")
    # Creating a dummy image for demonstration if file not found
    image = np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8)
else:
    image = cv.imread(path)

# median filter (ksize) should be odd numbers
image_median = cv.medianBlur(image, 5)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))
plt.title('Original Image')

plt.subplot(1, 2, 2)
plt.imshow(cv.cvtColor(image_median, cv.COLOR_BGR2RGB))
plt.title('Median Filtered Image')

plt.show()
