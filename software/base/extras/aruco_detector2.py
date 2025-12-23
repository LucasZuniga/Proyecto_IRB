# Based on:
# https://github.com/Ziad-Abaza/ArUco-Marker-Detection-Pose-Estimation/tree/main

# OpenCV version: 4.6.0

import cv2
import math

ArucoType: dict = {
    'DICT_4X4_50': cv2.aruco.DICT_4X4_50,
    'DICT_4X4_100': cv2.aruco.DICT_4X4_100,
    'DICT_4X4_250': cv2.aruco.DICT_4X4_250,
    'DICT_4X4_1000': cv2.aruco.DICT_4X4_1000,
    'DICT_5X5_50': cv2.aruco.DICT_5X5_50,
    'DICT_5X5_100': cv2.aruco.DICT_5X5_100,
    'DICT_5X5_250': cv2.aruco.DICT_5X5_250,
    'DICT_5X5_1000': cv2.aruco.DICT_5X5_1000,
    'DICT_6X6_50': cv2.aruco.DICT_6X6_50,
    'DICT_6X6_100': cv2.aruco.DICT_6X6_100,
    'DICT_6X6_250': cv2.aruco.DICT_6X6_250,
    'DICT_6X6_1000': cv2.aruco.DICT_6X6_1000,
    'DICT_7X7_50': cv2.aruco.DICT_7X7_50,
    'DICT_7X7_100': cv2.aruco.DICT_7X7_100,
    'DICT_7X7_250': cv2.aruco.DICT_7X7_250,
    'DICT_7X7_1000': cv2.aruco.DICT_7X7_1000,
    'DICT_ARUCO_ORIGINAL': cv2.aruco.DICT_ARUCO_ORIGINAL,
    'DICT_APRILTAG_16h5': cv2.aruco.DICT_APRILTAG_16h5,
    'DICT_APRILTAG_25h9': cv2.aruco.DICT_APRILTAG_25h9,
    'DICT_APRILTAG_36h10': cv2.aruco.DICT_APRILTAG_36h10,
    'DICT_APRILTAG_36h11': cv2.aruco.DICT_APRILTAG_36h11,
}


class ArUco_Marker():
    def __init__(self, corners, id):
        self.id = id
        self.corners = corners
        self.tl = corners[0][0]
        self.tr = corners[0][1]
        self.bl = corners[0][2]
        self.br = corners[0][3]
        
        self.get_centre()
        self.get_angle()
        
    def get_centre(self):
        top_centre_x = int((self.tl[0] + self.tr[0])/2)
        top_centre_y = int((self.tl[1] + self.tr[1])/2)
        self.top_centre = (top_centre_x, top_centre_y)
        
        bot_centre_x = int((self.bl[0] + self.br[0])/2)
        bot_centre_y = int((self.bl[1] + self.br[1])/2)
        self.bot_centre = (bot_centre_x, bot_centre_y)
        
        self.rigth_centre = (int((self.tr[0] + self.br[0])/2), int((self.tr[1] + self.br[1])/2))
        
        self.centre = (int((top_centre_x + bot_centre_x)/2), int((top_centre_y + bot_centre_y)/2))
        
    def get_angle(self):
        dx = self.top_centre[0] - self.centre[0]
        dy = self.top_centre[1] - self.centre[1]

        theta_rad = round((math.atan2(dy, dx)/2), 3)
        theta_deg = int((theta_rad/math.pi)*360)

        self.angle = theta_deg
        
    def draw_marker(self, frame):
        cv2.line(frame, self.centre, self.top_centre, (255, 0, 0), 2)
        cv2.putText(frame, f"ID: {self.id}, {self.angle} deg", (int(self.tl[0]), int(self.tl[1]) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2, )

     
class ArUco_Detector():
    def __init__(self):
        pass
    
    def aruco_marker_pose_estimation(self,aruco_type): 
        print('Detecting ArUco Marker...')
        cap = cv2.VideoCapture(0)
        aruco_dict = cv2.aruco.Dictionary_get(aruco_type)
        aruco_params = cv2.aruco.DetectorParameters_create()
        
        while True: 
            ret, frame = cap.read() 
        
            if not ret: 
                break 

            frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            corners, ids, _ = cv2.aruco.detectMarkers(frame_gray, aruco_dict, parameters= aruco_params)
            
            if ids is not None:
                for i in range(len(ids)):
                    new_marker = ArUco_Marker(corners[i], ids[i])
                    new_marker.draw_marker(frame)
                    
            cv2.imshow('ArUco Detection',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break


def run_aruco_marker_pose_estimation(aruco_type): 
    aruco_marker = ArUco_Detector() 
    aruco_marker.aruco_marker_pose_estimation(aruco_type)

if __name__ == '__main__': 
    run_aruco_marker_pose_estimation(ArucoType["DICT_4X4_1000"]) 