# Based on:
# https://github.com/Ziad-Abaza/ArUco-Marker-Detection-Pose-Estimation/tree/main

from enum import Enum
import cv2
import numpy as np 
import os 
import matplotlib.pyplot as plt 

class ArucoType(Enum):
    DICT_4X4_50 = cv2.aruco.DICT_4X4_50
    DICT_4X4_100 = cv2.aruco.DICT_4X4_100
    DICT_4X4_250 = cv2.aruco.DICT_4X4_250
    DICT_4X4_1000 = cv2.aruco.DICT_4X4_1000
    DICT_5X5_50 = cv2.aruco.DICT_5X5_50
    DICT_5X5_100 = cv2.aruco.DICT_5X5_100
    DICT_5X5_250 = cv2.aruco.DICT_5X5_250
    DICT_5X5_1000 = cv2.aruco.DICT_5X5_1000
    DICT_6X6_50 = cv2.aruco.DICT_6X6_50
    DICT_6X6_100 = cv2.aruco.DICT_6X6_100
    DICT_6X6_250 = cv2.aruco.DICT_6X6_250
    DICT_6X6_1000 = cv2.aruco.DICT_6X6_1000
    DICT_7X7_50 = cv2.aruco.DICT_7X7_50
    DICT_7X7_100 = cv2.aruco.DICT_7X7_100
    DICT_7X7_250 = cv2.aruco.DICT_7X7_250
    DICT_7X7_1000 = cv2.aruco.DICT_7X7_1000
    DICT_ARUCO_ORIGINAL = cv2.aruco.DICT_ARUCO_ORIGINAL
    DICT_APRILTAG_16h5 = cv2.aruco.DICT_APRILTAG_16h5
    DICT_APRILTAG_25h9 = cv2.aruco.DICT_APRILTAG_25h9
    DICT_APRILTAG_36h10 = cv2.aruco.DICT_APRILTAG_36h10
    DICT_APRILTAG_36h11 = cv2.aruco.DICT_APRILTAG_36h11

class ArucoMarkers(): 
    def __init__(self): 
        self.dir = os.path.dirname(os.path.abspath(__file__))

    def aruco_marker_pose_estimation(self,aruco_type,camera_matrix,dist_coeffs): 
        print('Detecting ArUco Marker...')
        cap = cv2.VideoCapture(0)
        aruco_dict = cv2.aruco.Dictionary_get(aruco_type.value)
        aruco_params = cv2.aruco.DetectorParameters_create()
        # detector = cv2.aruco.ArucoDetector(aruco_dict,aruco_params)

        world_points = np.array([[0.,0.,0.], # top left
                                 [1.,0.,0.], # top right
                                 [1.,1.,0.], # bottom right
                                 [0.,1.,0.]  # bottom left
        ])
        while True: 
            ret, frame = cap.read() 
        
            if not ret: 
                break 

            frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            corners, ids, _ = cv2.aruco.detectMarkers(frame_gray, aruco_dict, parameters= aruco_params)

            if ids is not None: 
                frame = cv2.aruco.drawDetectedMarkers(frame,corners,ids)

                for corner in corners: 
                    _,rvecs,tvecs = cv2.solvePnP(world_points,corner,camera_matrix,dist_coeffs)
                    rotation_matrix, _ = cv2.Rodrigues(rvecs)
                    flip_matrix = np.array([
                                    [0, 1, 0],
                                    [1, 0, 0],
                                    [0, 0, -1]
                                  ], dtype=np.float32)
                    transformed_rotation_matrix = rotation_matrix @ flip_matrix
                    rvecs_transformed, _ = cv2.Rodrigues(transformed_rotation_matrix)

                    cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvecs_transformed, tvecs, 1)  

            cv2.imshow('ArUco Detection',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break

def run_aruco_marker_pose_estimation(aruco_type): 
    aruco_marker = ArucoMarkers() 
    # Logitech Camera Calibration (Need to calibrate for your own camera)
    camera_matrix = np.array([
        [1432.0, 0.0,    983.0], 
        [0.0,    1434.0, 561.0], 
        [0.0,    0.0,    1.0]
    ])  
    dist_coeffs = np.array([0.05994318, -0.26432366, -0.00135378, -0.00081574,  0.29707202])
    aruco_marker.aruco_marker_pose_estimation(aruco_type,camera_matrix,dist_coeffs)

if __name__ == '__main__': 
    run_aruco_marker_pose_estimation(ArucoType.DICT_4X4_1000) 