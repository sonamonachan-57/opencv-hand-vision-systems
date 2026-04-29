# need to install opencv       // pip install opencv-contrib-python





import os
import sys

venv_path = '/home/sona-inc5619/yolo_env/lib/python3.12/site-packages'
if os.path.exists(venv_path) and venv_path not in sys.path:
    sys.path.insert(0, venv_path)







import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

# Version-safe MultiTracker
def create_multitracker():
    if hasattr(cv2, "legacy"):
        return cv2.legacy.MultiTracker_create()
    else:
        return cv2.MultiTracker_create()

# Version-safe CSRT
def create_csrt():
    if hasattr(cv2, "legacy"):
        return cv2.legacy.TrackerCSRT_create()
    else:
        return cv2.TrackerCSRT_create()

multi_tracker = create_multitracker()   

detect_interval = 20
frame_count = 0

target_classes = ["person", "cell phone"]

while True:
    success, frame = cap.read()
    if not success:
        break

    frame_count += 1

    # Detection step
    if frame_count % detect_interval == 0:
        results = model(frame)[0]

        multi_tracker = create_multitracker()   # reset tracker

        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            if label in target_classes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                w, h = x2 - x1, y2 - y1

                tracker = create_csrt()
                multi_tracker.add(tracker, frame, (x1, y1, w, h))

    # Tracking step
    success, boxes = multi_tracker.update(frame)

    for box in boxes:
        x, y, w, h = [int(v) for v in box]
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

    cv2.imshow("YOLO Detection + Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()