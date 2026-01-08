import cv2 as cv
import numpy as np
import os
import matplotlib.pyplot as plt

path = './images/coins.jpg'
if not os.path.exists(path):
    print(f'File {path} not found')
    # Creating a dummy image for demonstration if file not found
    image = np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8)
else:
    image = cv.imread(path)

# Different Laplacian masks
mask1 = np.array([[0, -1, 0],
                  [-1, 4, -1],
                  [0, -1, 0]])

mask2 = np.array([[-1, -1, -1],
                  [-1, 8, -1],
                  [-1, -1, -1]])

mask3 = np.array([[-2, -1, -2],
                  [-1, 4, -1],
                  [-2, -1, -2]])

image_sharp1 = cv.filter2D(image, -1, mask1)
image_sharp2 = cv.filter2D(image, -1, mask2)
image_sharp3 = cv.filter2D(image, -1, mask3)

plt.figure(figsize=(15, 5))
plt.subplot(1, 4, 1)
plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))
plt.title('Original Image')

plt.subplot(1, 4, 2)
plt.imshow(cv.cvtColor(image_sharp1, cv.COLOR_BGR2RGB))
plt.title('Sharp 1')

plt.subplot(1, 4, 3)
plt.imshow(cv.cvtColor(image_sharp2, cv.COLOR_BGR2RGB))
plt.title('Sharp 2')

plt.subplot(1, 4, 4)
plt.imshow(cv.cvtColor(image_sharp3, cv.COLOR_BGR2RGB))
plt.title('Sharp 3')

plt.show()
