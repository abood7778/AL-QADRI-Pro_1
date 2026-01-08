import cv2 as cv
import numpy as np
import os
import matplotlib.pyplot as plt

path = './images/natural.jpg'
if not os.path.exists(path):
    print(f'File {path} not found')
    # Creating a dummy image for demonstration if file not found
    image = np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8)
else:
    image = cv.imread(path)

# Different Laplacian masks
mask_vertical = np.array([[0, 1, 0],
                          [0, 1, 0],
                          [0, -1, 0]])

mask_horizontal = np.array([[0, 0, 0],
                            [1, 1, -1],
                            [0, 0, 0]])

mask_dig1 = np.array([[1, 0, 0],
                      [0, 1, 0],
                      [0, 0, -1]])

mask_dig2 = np.array([[0, 0, 1],
                      [0, 1, 0],
                      [-1, 0, 0]])

image_diff1 = cv.filter2D(image, -1, mask_vertical)
image_diff2 = cv.filter2D(image_diff1, -1, mask_horizontal)
image_diff3 = cv.filter2D(image, -1, mask_dig1)
image_diff4 = cv.filter2D(image_diff3, -1, mask_dig2)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))
plt.title('Original Image')

plt.subplot(1, 2, 2)
plt.imshow(cv.cvtColor(image_diff4, cv.COLOR_BGR2RGB))
plt.title('Difference Filtered')

plt.show()
