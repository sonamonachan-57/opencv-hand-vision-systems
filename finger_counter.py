import os
import sys
venv_path = '/home/sona-inc5619/mp_env/lib/python3.12/site-packages'
if os.path.exists(venv_path) and venv_path not in sys.path:
    sys.path.insert(0, venv_path)

import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=2)
mpDraw = mp.solutions.drawing_utils

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    totalFingers = 0

    if results.multi_hand_landmarks:
        for handNo, handLms in enumerate(results.multi_hand_landmarks):

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            lmList = []
            h, w, c = img.shape

            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])

            if len(lmList) != 0:
                fingers = []

                #  Thumb
                if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                #  Other 4 fingers
                for id in range(1, 5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                totalFingers += sum(fingers)

    #  Display count
    cv2.rectangle(img, (20, 20), (200, 120), (0,255,0), cv2.FILLED)
    cv2.putText(img, str(totalFingers), (45,100),
                cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,0), 5)

    cv2.imshow("Finger Counter", img)
    cv2.waitKey(1)