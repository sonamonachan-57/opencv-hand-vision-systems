
import os
import sys
venv_path = '/home/sona-inc5619/mp_env/lib/python3.12/site-packages'
if os.path.exists(venv_path) and venv_path not in sys.path:
    sys.path.insert(0, venv_path)
import cv2
import mediapipe as mp

# Initialize camera
cap = cv2.VideoCapture(0)

# MediaPipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

mpDraw = mp.solutions.drawing_utils

while True:

    success, img = cap.read()
    if not success:
        break

    # Convert BGR → RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detect hands
    results = hands.process(imgRGB)

    # Draw hand landmarks
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:

            mpDraw.draw_landmarks(
                img,
                handLms,
                mpHands.HAND_CONNECTIONS
            )

    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
    
    
    
    #this python code converted into ros2 node
    


# import cv2
# import mediapipe as mp
# import rclpy
# from rclpy.node import Node
# from sensor_msgs.msg import Image
# from cv_bridge import CvBridge


# class HandDetector(Node):
#     def __init__(self):
#         super().__init__('hand_detector_node')
#         self.bridge = CvBridge()
#         self.subscription = self.create_subscription(
#             Image,
#             '/image_raw',
#             self.image_callback,
#             10
#         )

#         self.mpHands = mp.solutions.hands
#         self.hands = self.mpHands.Hands()
#         self.mpDraw = mp.solutions.drawing_utils

#     def image_callback(self, msg):

#         # Convert ROS Image → OpenCV image
#         img = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

#         imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         results = self.hands.process(imgRGB)

#         if results.multi_hand_landmarks:
#             for handLms in results.multi_hand_landmarks:
#                 self.mpDraw.draw_landmarks(
#                     img,
#                     handLms,
#                     self.mpHands.HAND_CONNECTIONS
#                 )

#         cv2.imshow("Hand Detection", img)
#         cv2.waitKey(1)


# def main(args=None):
#     rclpy.init(args=args)
#     node = HandDetector()
#     rclpy.spin(node)
#     node.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()

    