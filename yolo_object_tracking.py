import os
import sys

venv_path = '/home/sona-inc5619/mp_env/lib/python3.12/site-packages'
if os.path.exists(venv_path) and venv_path not in sys.path:
    sys.path.insert(0, venv_path)


import cv2
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO("yolov8n.pt")   # nano model = fastest

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO tracking
    results = model.track(frame, persist=True)

    # Get result for current frame
    result = results[0]

    boxes = result.boxes

    if boxes is not None:
        for box in boxes:

            # Bounding box
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Object class
            cls = int(box.cls[0])
            class_name = model.names[cls]

            # Tracking ID
            track_id = int(box.id[0]) if box.id is not None else -1

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)

            # Label text
            label = f"{class_name} ID:{track_id}"

            # Draw label
            cv2.putText(frame, label,
                        (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0,255,0),
                        2)

    # Show frame
    cv2.imshow("YOLOv8 Object Tracking", frame)

    # Exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()