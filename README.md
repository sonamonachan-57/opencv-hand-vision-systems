# 1. ✋ Hand Tracking using OpenCV and MediaPipe

## 📌 Overview

This project demonstrates **real-time hand detection and tracking** using **OpenCV** and **MediaPipe Hands**. The system captures video from a webcam, detects hands in each frame, and overlays **21 hand landmarks** along with their skeletal connections.

MediaPipe’s hand tracking model is optimized for **real-time performance ⚡** and can track multiple hands simultaneously, making it suitable for applications such as **gesture recognition, virtual control systems, and human–computer interaction 🤖**.

---

## ✨ Features

*  Real-time **hand detection and tracking**
*  Detects **up to 2 hands simultaneously**
*  Displays **21 hand landmarks per hand**
*  Draws **hand skeleton connections**
*  Works with a **webcam feed**
*  Lightweight and **runs in real time**

---

##  Technologies Used

*  **Python**
*  **OpenCV** – for video capture and display
*  **MediaPipe** – for hand detection and landmark tracking

---

## 📦 Installation



### Install dependencies

```bash
pip install opencv-python mediapipe
```

---


## ⚙️ How It Works

1️⃣ The webcam captures frames using **OpenCV 📷**
2️⃣ Each frame is converted from **BGR → RGB 🎨** format
3️⃣ MediaPipe processes the frame to detect hands ✋
4️⃣ If hands are detected:

* 📍 **21 hand landmarks** are identified
* 🔗 Landmarks and their connections are drawn on the frame
  5️⃣ The processed frame is displayed in a window 🖥️

---

## 🖐 Hand Landmark Structure

Each detected hand contains **21 landmarks**, representing key points on the hand.

Examples:

| 🔢 Landmark ID | 📍 Description      |
| -------------- | ------------------- |
| 0              | Wrist               |
| 4              | Thumb Tip           |
| 8              | Index Finger Tip    |
| 12             | Middle Finger Tip   |
| 16             | Ring Finger Tip     |
| 20             | Pinky Tip           |

These landmarks can be used for:

*  Gesture recognition
*  Finger tracking
*  Distance measurement between fingers
*  Human–computer interaction systems

---

## 🚀 Applications

This hand tracking system can be extended to build:

*  **Hand gesture recognition**
*  **Virtual mouse**
*  **Finger-based volume control**
*  **Sign language recognition**
*  **Augmented reality interactions**
*  **Robotics control using gestures**

---

## 🖥 Output:



## 🙌 Acknowledgements

* 🧠 **Google MediaPipe** for providing the hand tracking model
* 📷 **OpenCV** for real-time image processing
