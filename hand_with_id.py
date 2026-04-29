import os
import sys
venv_path = '/home/sona-inc5619/mp_env/lib/python3.12/site-packages'
if os.path.exists(venv_path) and venv_path not in sys.path:
    sys.path.insert(0, venv_path)
import subprocess


import cv2
import mediapipe as mp
import math

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=5)
mpDraw = mp.solutions.drawing_utils

# Tracking variables
hand_centers_prev = {}
next_hand_id = 0

def get_hand_center(lmList):
    xs = [lm[1] for lm in lmList]
    ys = [lm[2] for lm in lmList]
    return int(sum(xs)/len(xs)), int(sum(ys)/len(ys))

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    hand_centers_curr = {}

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            lmList = []
            h, w, c = img.shape

            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((id, cx, cy))

            if len(lmList) >= 9:
               

                #  Hand tracking
                center = get_hand_center(lmList)

                assigned_id = None
                for prev_id, prev_center in hand_centers_prev.items():
                    dist = math.hypot(center[0]-prev_center[0], center[1]-prev_center[1])
                    if dist < 60:   # distance threshold
                        assigned_id = prev_id
                        break

                if assigned_id is None:
                    assigned_id = next_hand_id
                    next_hand_id += 1

                hand_centers_curr[assigned_id] = center

                # Draw ID
                cv2.putText(img, f'ID {assigned_id}', (center[0]-20, center[1]-20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    hand_centers_prev = hand_centers_curr

    cv2.imshow("Image", img)
    cv2.waitKey(1)