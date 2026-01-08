import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import os

path = './images/houghlines5.jpg'
if not os.path.exists(path):
    print(f'The Path {path} not found')
    # Creating a dummy image for demonstration if file not found
    image = np.zeros((300, 300, 3), dtype=np.uint8)
    cv.line(image, (50, 50), (250, 250), (255, 255, 255), 2)
else:
    image = cv.imread(path)

gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
edges = cv.Canny(gray, 50, 150)
lines = cv.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=20, minLineLength=40, maxLineGap=5)

if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

plt.figure(figsize=(10, 10))
plt.subplot(1, 2, 1)
plt.title('Edges Image')
plt.imshow(edges, cmap='gray')

plt.subplot(1, 2, 2)
plt.title('Hough Lines Image')
plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))

plt.show()
