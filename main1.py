import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("لا يمكن فتح الكاميرا")
else:
    print("اضغط 'q' للخروج")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("انتهى الفيديو أو لا توجد كاميرا")
            break
        cv2.imshow("Basic Video Player", frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()