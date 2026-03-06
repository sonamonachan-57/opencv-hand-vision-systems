import cv2
import mediapipe as mp
import numpy as np
import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# Path to the gesture model
model_path = "gesture_recognizer.task"


# -------- Setup Gesture Recognizer --------
base_options = python.BaseOptions(model_asset_path=model_path)

options = vision.GestureRecognizerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1
)

recognizer = vision.GestureRecognizer.create_from_options(options)


# -------- Webcam --------
cap = cv2.VideoCapture(0)

# Control FPS
prev_time = 0
fps_limit = 10

while cap.isOpened():

    current_time = time.time()

    if current_time - prev_time < 1/fps_limit:
        continue

    prev_time = current_time

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame,1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=np.array(rgb)
    )

    timestamp = int(time.time()*1000)

    result = recognizer.recognize_for_video(mp_image, timestamp)

    gesture_name = "None"

    if result.gestures:

        gesture = result.gestures[0][0]

        if gesture.score > 0.3:
            gesture_name = gesture.category_name

    # Draw gesture text
    cv2.putText(
        frame,
        f'Gesture: {gesture_name}',
        (20,60),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,0),
        2
    )

    cv2.imshow("Hand Gesture Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
