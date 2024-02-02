import numpy as np
import cv2, os
import matplotlib.pyplot as plt
import matplotlib as mpl


#datadir = "ArUco_Cube/data/"


aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
board = cv2.aruco.CharucoBoard_create(5, 7, 2.72, 1.65, aruco_dict)
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
imboard = board.draw((2000, 2000))

#plt.imshow(imboard, cmap = mpl.cm.gray, interpolation = "nearest")
#ax.axis("off")
#plt.show()

# only in here for debugging
#images = np.array([dir + f for f in os.listdir(dir) if f.endswith(".jpg") or f.endswith(".png")])


def read_chessboards(dir):

    print("POSE ESTIMATION STARTS:")
    allCorners = []
    allIds = []
    decimator = 0
    # SUB PIXEL CORNER DETECTION CRITERION
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.00001)

    images = np.array([dir + f for f in os.listdir(dir) if f.endswith(".jpg") or f.endswith(".png")])

    for im in images:
        print("=> Processing image {0}".format(im))
        frame = cv2.imread(im)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict)


        if corners is None or ids is None:
            continue

        if len(corners)>0:

            # SUB PIXEL DETECTION
            for corner in corners:
                cv2.cornerSubPix(gray, corner,
                                 winSize = (3,3),
                                 zeroZone = (-1,-1),
                                 criteria = criteria)
                
            res2 = cv2.aruco.interpolateCornersCharuco(corners,ids,gray,board)
            if res2[1] is not None and res2[2] is not None and len(res2[1])>3 and decimator%1==0:
                allCorners.append(res2[1])
                allIds.append(res2[2])

        decimator+=1

    imsize = gray.shape
    return allCorners,allIds,imsize



def calibrate_camera(allCorners,allIds,imsize):
    """
    Calibrates the camera using the dected corners.
    """
    print("CAMERA CALIBRATION")

    cameraMatrixInit = np.array([[ 1000.,    0., imsize[0]/2.],
                                 [    0., 1000., imsize[1]/2.],
                                 [    0.,    0.,           1.]])

    distCoeffsInit = np.zeros((5,1))
    flags = (cv2.CALIB_USE_INTRINSIC_GUESS + cv2.CALIB_RATIONAL_MODEL + cv2.CALIB_FIX_ASPECT_RATIO)

    (ret, camera_matrix, distortion_coefficients0,
     rotation_vectors, translation_vectors, _, _, _) = cv2.aruco.calibrateCameraCharucoExtended(
                      charucoCorners=allCorners,
                      charucoIds=allIds,
                      board=board,
                      imageSize=imsize,
                      cameraMatrix=cameraMatrixInit,
                      distCoeffs=distCoeffsInit,
                      flags=flags,
                      criteria=(cv2.TERM_CRITERIA_EPS & cv2.TERM_CRITERIA_COUNT, 10000, 1e-9))

    return ret, camera_matrix, distortion_coefficients0, rotation_vectors, translation_vectors



# dir is the directory where all images are stored
def start_calibration(dir):

    all_corners, all_ids, imsize = read_chessboards(dir)
    return calibrate_camera(all_corners,all_ids,imsize)


#ret, mtx, dist, rvecs, tvecs = start_calibration(datadir) # this is how you would call this function from outside

# TODO 1: Better images and double-check chosen parameters
# TODO 2: 



# This code here displays the distorted and the corrected images, only here for debugging
"""
i=1 # select image id
for i in range(0, 18, 2):
    plt.figure()
    frame = cv2.imread(images[i])
    img_undist = cv2.undistort(frame,mtx,dist,None)
    plt.subplot(1,2,1)
    plt.imshow(frame)
    plt.title("Raw image")
    plt.axis("off")
    plt.subplot(1,2,2)
    plt.imshow(img_undist)
    plt.title("Corrected image")
    plt.axis("off")
    plt.show()
    """