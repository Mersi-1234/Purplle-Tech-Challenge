from ultralytics import YOLO
import cv2
import random
import time

from event_generator import save_event

model = YOLO("yolov8n.pt")

VIDEO_PATH = r"data\Store 1\CAM 3 - entry.mp4"

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("ERROR: Video not found or cannot be opened!")
    exit()

person_present = False
current_visitor = None
entry_time = None

zone_sent = False
billing_sent = False

missing_frames = 0
EXIT_THRESHOLD = 30

while True:

    ret, frame = cap.read()

    if not ret:
        print("Video Finished")
        break

    results = model(frame, verbose=False)

    boxes = results[0].boxes

    people_count = 0

    for box in boxes:
        cls = int(box.cls[0])

        if cls == 0:      # person class only
            people_count += 1

    # -----------------------------
    # ENTRY
    # -----------------------------
    if people_count > 0:

        missing_frames = 0

        if not person_present:

            current_visitor = f"VIS{random.randint(100,999)}"

            save_event(current_visitor, "ENTRY")

            print(f"{current_visitor} ENTERED")

            person_present = True
            entry_time = time.time()

            zone_sent = False
            billing_sent = False

    else:

        if person_present:
            missing_frames += 1

    # -----------------------------
    # CUSTOMER JOURNEY
    # -----------------------------
    if person_present:

        elapsed = time.time() - entry_time

        if elapsed > 3 and not zone_sent:

            save_event(current_visitor, "ZONE_VISIT")

            print(f"{current_visitor} VISITED ZONE")

            zone_sent = True

        if elapsed > 6 and not billing_sent:

            save_event(current_visitor, "BILLING")

            print(f"{current_visitor} BILLING")

            billing_sent = True

    # -----------------------------
    # EXIT
    # -----------------------------
    if person_present and missing_frames > EXIT_THRESHOLD:

        save_event(current_visitor, "EXIT")

        print(f"{current_visitor} EXITED")

        person_present = False
        current_visitor = None
        entry_time = None

        zone_sent = False
        billing_sent = False

        missing_frames = 0

    annotated_frame = results[0].plot()

    cv2.putText(
        annotated_frame,
        f"Visitors Detected: {people_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow(
        "Purplle Store Intelligence",
        annotated_frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()