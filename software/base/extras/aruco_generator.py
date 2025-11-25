# You can also generate and download ArUco markers from this link:
# https://chev.me/arucogen/

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Define the dictionary we want to use
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_1000)

# Generate a marker
marker_id = 0
marker_size = 200       # Size in pixels
marker_image = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size)

cv2.imwrite(f"marker_{marker_id}.png", marker_image)
plt.imshow(marker_image, cmap= "gray", interpolation= "nearest")
plt.axis("off")
plt.title(f"ArUco Marker {marker_id}")
plt.show()