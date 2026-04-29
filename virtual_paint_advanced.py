import os
import sys

venv_path = '/home/sona-inc5619/mp_env/lib/python3.12/site-packages'
if os.path.exists(venv_path) and venv_path not in sys.path:
    sys.path.insert(0, venv_path)


import cv2
import mediapipe as mp
import numpy as np
import time

# Camera
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

# Mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1,min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Canvas
canvas = np.zeros((720,1280,3),np.uint8)

drawColor = (255,0,255)
brushThickness = 10
eraserThickness = 60

xp,yp = 0,0
history = []

# Tool buttons
buttons = {
"brush":(10,10,110,60),
"eraser":(120,10,220,60),
"undo":(230,10,330,60),
"save":(340,10,440,60),
"clear":(450,10,550,60)
}

# Color palette
palette = [
((255,0,0),(600,10,660,60)),   # blue
((0,255,0),(670,10,730,60)),   # green
((0,0,255),(740,10,800,60)),   # red
((0,255,255),(810,10,870,60)), # yellow
((255,0,255),(880,10,940,60)), # purple
((0,0,0),(950,10,1010,60))     # black (eraser)
]

def draw_ui(img):

    # Buttons
    cv2.rectangle(img,(10,10),(110,60),(200,200,200),-1)
    cv2.putText(img,"Brush",(20,45),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,0),2)

    cv2.rectangle(img,(120,10),(220,60),(200,200,200),-1)
    cv2.putText(img,"Erase",(130,45),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,0),2)

    cv2.rectangle(img,(230,10),(330,60),(200,200,200),-1)
    cv2.putText(img,"Undo",(250,45),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,0),2)

    cv2.rectangle(img,(340,10),(440,60),(200,200,200),-1)
    cv2.putText(img,"Save",(360,45),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,0),2)

    cv2.rectangle(img,(450,10),(550,60),(200,200,200),-1)
    cv2.putText(img,"Clear",(470,45),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,0),2)

    # Color palette
    for color,(x1,y1,x2,y2) in palette:
        cv2.rectangle(img,(x1,y1),(x2,y2),color,-1)

def check_button(x,y):
    for name,(x1,y1,x2,y2) in buttons.items():
        if x1 < x < x2 and y1 < y < y2:
            return name
    return None

def check_palette(x,y):
    for color,(x1,y1,x2,y2) in palette:
        if x1 < x < x2 and y1 < y < y2:
            return color
    return None

def recognize_shape(canvas):

    gray = cv2.cvtColor(canvas,cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,50,255,cv2.THRESH_BINARY)

    contours,_ = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:

        area = cv2.contourArea(cnt)
        if area < 1000:
            continue

        peri = cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,0.02*peri,True)

        x,y,w,h = cv2.boundingRect(approx)

        if len(approx)==4:
            cv2.putText(canvas,"Rectangle",(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

        elif len(approx)>6:
            cv2.putText(canvas,"Circle",(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

while True:

    success,img = cap.read()
    img = cv2.flip(img,1)

    draw_ui(img)

    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:

        for handLms in results.multi_hand_landmarks:

            lmList=[]
            for id,lm in enumerate(handLms.landmark):

                h,w,c = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                lmList.append((cx,cy))

            if len(lmList)!=0:

                x1,y1 = lmList[8]
                x2,y2 = lmList[12]

                fingers=[]

                if lmList[8][1] < lmList[6][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                if lmList[12][1] < lmList[10][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # Selection mode
                if fingers[0] and fingers[1]:

                    xp,yp = 0,0

                    button = check_button(x1,y1)
                    color = check_palette(x1,y1)

                    if color is not None:
                        drawColor = color

                    if button == "brush":
                        brushThickness = 10

                    elif button == "eraser":
                        drawColor = (0,0,0)

                    elif button == "undo":
                        if history:
                            canvas[:] = history.pop()

                    elif button == "save":
                        name = f"drawing_{int(time.time())}.png"
                        cv2.imwrite(name,canvas)

                    elif button == "clear":
                        canvas[:] = 0

                # Drawing mode
                if fingers[0] and not fingers[1]:

                    cv2.circle(img,(x1,y1),10,drawColor,-1)

                    if xp==0 and yp==0:
                        xp,yp = x1,y1

                    history.append(canvas.copy())

                    if drawColor==(0,0,0):
                        cv2.line(canvas,(xp,yp),(x1,y1),drawColor,eraserThickness)
                    else:
                        cv2.line(canvas,(xp,yp),(x1,y1),drawColor,brushThickness)

                    xp,yp = x1,y1

            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)

    recognize_shape(canvas)

    gray = cv2.cvtColor(canvas,cv2.COLOR_BGR2GRAY)
    _,inv = cv2.threshold(gray,50,255,cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv,cv2.COLOR_GRAY2BGR)

    img = cv2.bitwise_and(img,inv)
    img = cv2.bitwise_or(img,canvas)

    cv2.imshow("AI Virtual Whiteboard",img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()