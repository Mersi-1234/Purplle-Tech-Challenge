import cv2

video = r"data\Store 1\CAM 3 - entry.mp4"

cap = cv2.VideoCapture(video)

if not cap.isOpened():
    print("Video not opening")
else:
    print("Video opened successfully")

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        cv2.imshow("Video", frame)

        if cv2.waitKey(30) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()