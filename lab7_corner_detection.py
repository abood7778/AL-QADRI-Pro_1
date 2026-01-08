import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import os

path = './images/corners.png'
if not os.path.exists(path):
    print(f'The Path {path} not found')
    # Creating a dummy image for demonstration if file not found
    image = np.zeros((300, 300, 3), dtype=np.uint8)
    cv.rectangle(image, (50, 50), (250, 250), (255, 255, 255), 2)
else:
    image = cv.imread(path)

gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
corners = cv.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.01, minDistance=10)

if corners is not None:
    corners = np.intp(corners)
    for c in corners:
        x, y = c.ravel()
        cv.circle(image, (x, y), 4, (0, 255, 0), -1)

plt.figure(figsize=(10, 10))
plt.subplot(1, 2, 1)
plt.title('Original Image')
plt.imshow(cv.cvtColor(cv.imread(path) if os.path.exists(path) else np.zeros((300,300,3), np.uint8), cv.COLOR_BGR2RGB))

plt.subplot(1, 2, 2)
plt.title('Corner Detection Image')
plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))

plt.show()
