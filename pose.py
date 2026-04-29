import os
import sys

venv_path = '/home/sona-inc5619/mp_env/lib/python3.12/site-packages'
if os.path.exists(venv_path) and venv_path not in sys.path:
    sys.path.insert(0, venv_path)

import cv2
import mediapipe as mp
#import time


cap=cv2.VideoCapture(0)
mpPose=mp.solutions.pose
pose=mpPose.Pose()
mpDraw=mp.solutions.drawing_utils

#PTime=0
while True:
    success,img=cap.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=pose.process(imgRGB)
    print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS)
        
        cv2.imshow("posedetector",img)
    cv2.waitKey(1)
    
    
    
    
    
    #this python code converted to ros2 node
    
# import os
# import sys

# venv_path = '/home/sona-inc5619/mp_env/lib/python3.12/site-packages'
# if os.path.exists(venv_path) and venv_path not in sys.path:
#     sys.path.insert(0, venv_path)

# import cv2
# import mediapipe as mp
# import rclpy
# from rclpy.node import Node
# from cv_bridge import CvBridge
# from sensor_msgs.msg import Image


# class PoseDetector(Node):
    
#  def __init__(self):
#        super().__init__('pose_detector_node')

#         self.bridge = CvBridge()

#         self.subscription = self.create_subscription(
#             Image,
#             '/image_raw',
#             self.image_callback,
#             10
#         )

#         self.mpPose = mp.solutions.pose
#         self.pose = self.mpPose.Pose()
#         self.mpDraw = mp.solutions.drawing_utils

#     def image_callback(self, msg):
#         # ROS Image → OpenCV
#         img = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

#         imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         results = self.pose.process(imgRGB)

#         if results.pose_landmarks:
#             self.mpDraw.draw_landmarks(
#                 img,
#                 results.pose_landmarks,
#                 self.mpPose.POSE_CONNECTIONS
#             )

#         cv2.imshow("Pose Detector", img)
#         cv2.waitKey(1)


# def main(args=None):
#     rclpy.init(args=args)
#     node = PoseDetector()
#     rclpy.spin(node)

#     node.destroy_node()
#     cv2.destroyAllWindows()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()
