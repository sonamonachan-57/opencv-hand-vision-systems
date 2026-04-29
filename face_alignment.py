import os
import sys

venv_path = '/home/sona-inc5619/deep_env/lib/python3.12/site-packages'
if os.path.exists(venv_path) and venv_path not in sys.path:
    sys.path.insert(0, venv_path)

import cv2
import dlib
import math
from imutils import rotate_bound


cap = cv2.VideoCapture(0)

# Load dlib models

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

facePoints = [27, 30]  # Nose bridge points

def getAngle(points):
    if len(points) < 3:
        return 0
    
    b, c, a = points[-3:]
    ang = math.degrees(
        math.atan2(c[1]-b[1], c[0]-b[0]) - 
        math.atan2(a[1]-b[1], a[0]-b[0])
    )
    
    ang = round(ang + 360 if ang < 0 else ang)
    return ang


while True:
    ret, frame = cap.read()
    if not ret:
        break

    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(imgGray)

    angle = 0

    for face in faces:
        landmarks = predictor(imgGray, face)
        points = []

        for i in facePoints:
            x = landmarks.part(i).x
            y = landmarks.part(i).y
            points.append([x, y])

            if i == 27:
                points.append([x, y + 20])  #  reference point

            #  draw landmarks
            cv2.circle(frame, (x, y), 3, (0, 255, 0), cv2.FILLED)

        angle = getAngle(points)
        break  # align only first detected face

    # Rotate frame
    aligned = rotate_bound(frame, angle)

    # Display
    cv2.imshow("Original", frame)
    cv2.imshow("Aligned Face", aligned)

    if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
