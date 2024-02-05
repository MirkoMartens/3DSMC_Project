# 3DSMC_Project

IMPORTANT OPENCV FUNCTIONS:
+++calibrateCameraCharucoExtended():
Calibrate a camera using Charuco corners.
This function calibrates a camera using a set of corners of a Charuco Board. The function receives a list of detected corners and its identifiers from several views of the Board. The function returns the final re-projection error.

Opencv Link:
https://docs.opencv.org/3.4.18/d9/d6a/group__aruco.html#ga54cf81c2e39119a84101258338aa7383


+++detectMarkers():
Basic marker detection.
Performs marker detection in the input image. Only markers included in the specific dictionary (cv2.aruco.DICT_4X4_50) are searched. For each detected marker, it returns the 2D position of its corner in the image and its corresponding identifier. Note that this function does not perform pose estimation.

The function does not correct lens distortion or takes it into account. It's recommended to undistort input image with corresponging camera model, if camera parameters are known

Opencv Link:
https://docs.opencv.org/3.4.18/d9/d6a/group__aruco.html#ga061ee5b694d30fa2258dd4f13dc98129


+++solvePnP():
Finds an object pose from 3D-2D point correspondences.
This function returns the rotation and the translation vectors that transform a 3D point expressed in the object coordinate frame to the camera coordinate frame, using cv.SOLVEPNP_IPPE_SQUARE for markers:
Infinitesimal Plane-Based Pose Estimation [59]
This is a special case suitable for marker pose estimation.
4 coplanar object points must be defined in the following order:

point 0: [-squareLength / 2, squareLength / 2, 0]
point 1: [ squareLength / 2, squareLength / 2, 0]
point 2: [ squareLength / 2, -squareLength / 2, 0]
point 3: [-squareLength / 2, -squareLength / 2, 0]

Ref:
Toby Collins and Adrien Bartoli. Infinitesimal plane-based pose estimation. International Journal of Computer Vision, 109(3):252–286, 2014.

Opencv Link:
https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html#ga549c2075fac14829ff4a58bc931c033d

