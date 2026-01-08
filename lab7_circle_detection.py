import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import os

path = './images/planet_glow.jpg'
if not os.path.exists(path):
    print(f'The Path {path} not found')
    # Creating a dummy image for demonstration if file not found
    image = np.zeros((300, 300, 3), dtype=np.uint8)
    cv.circle(image, (150, 150), 50, (255, 255, 255), -1)
else:
    image = cv.imread(path)

gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
gray = cv.medianBlur(gray, 5)
circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, dp=1, minDist=120, param1=90, param2=40, minRadius=0, maxRadius=0)

if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        cv.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
        cv.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)

plt.figure(figsize=(10, 10))
plt.subplot(1, 2, 1)
plt.title('Original Image')
plt.imshow(cv.cvtColor(cv.imread(path) if os.path.exists(path) else np.zeros((300,300,3), np.uint8), cv.COLOR_BGR2RGB))

plt.subplot(1, 2, 2)
plt.title('Hough Circle Image')
plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))

plt.show()
