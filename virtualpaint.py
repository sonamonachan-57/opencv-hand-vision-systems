import os
import sys

venv_path = '/home/sona-inc5619/mp_env/lib/python3.12/site-packages'
if os.path.exists(venv_path) and venv_path not in sys.path:
    sys.path.insert(0, venv_path)


import cv2
import mediapipe as mp
import numpy as np

# Camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Mediapipe hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

# Drawing variables
drawColor = (255, 0, 255)
brushThickness = 15
eraserThickness = 50

xp, yp = 0, 0

imgCanvas = np.zeros((720,1280,3), np.uint8)

while True:

    success, img = cap.read()
    img = cv2.flip(img,1)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:

        for handLms in results.multi_hand_landmarks:

            lmList = []

            for id,lm in enumerate(handLms.landmark):

                h,w,c = img.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                lmList.append((cx,cy))

            if len(lmList) != 0:

                # Index finger tip
                x1,y1 = lmList[8]

                # Middle finger tip
                x2,y2 = lmList[12]

                # Check which fingers are up
                fingers = []

                if lmList[8][1] < lmList[6][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                if lmList[12][1] < lmList[10][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # Selection Mode (2 fingers)
                if fingers[0] == 1 and fingers[1] == 1:

                    xp, yp = 0, 0

                    cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)

                    if y1 < 100:

                        if 100 < x1 < 300:
                            drawColor = (255,0,255)

                        elif 350 < x1 < 550:
                            drawColor = (255,0,0)

                        elif 600 < x1 < 800:
                            drawColor = (0,255,0)

                        elif 850 < x1 < 1050:
                            drawColor = (0,0,0)

                # Drawing Mode (1 finger)
                if fingers[0] == 1 and fingers[1] == 0:

                    cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)

                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1

                    if drawColor == (0,0,0):
                        cv2.line(img,(xp,yp),(x1,y1),drawColor,eraserThickness)
                        cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,eraserThickness)
                    else:
                        cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
                        cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThickness)

                    xp, yp = x1, y1

            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)

    imgGray = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _,imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)

    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imgCanvas)

    cv2.imshow("Virtual Painter",img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break