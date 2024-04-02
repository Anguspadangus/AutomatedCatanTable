'''
Documentation:
After the image is undistorted, create the homograhy matrix. Then you are free to go form camera to world frame! 
May need to test what goes on with the robber since we are using the plane assumption

import numpy as np
import cv2

# With distortion corrected so we can map out 1 to 1
uv = np.array([[548,103], [337,143],[239,368],[515,279]])
xy = np.array([[0,0], [-500, -100], [-700,-600], [-100, -400]])

h, status = cv2.findHomography(xy, uv)

# im_pnt = np.array([337,143, 1])
im_pnt = np.array([380,188, 1])

wrld = np.matmul(np.linalg.inv(h), im_pnt)
print(wrld)

w_x = wrld[0] / wrld[2]
w_y = wrld[1] / wrld[2]

print(w_x, w_y)
'''
import cv2
# assert cv2.__version__[0] == '3', 'The fisheye module requires opencv version >= 3.0.0'
import numpy as np
import os
import glob
CHECKERBOARD = (8,14)
subpix_criteria = (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)
calibration_flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC+cv2.fisheye.CALIB_FIX_SKEW
objp = np.zeros((1, CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
_img_shape = None
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
fname = 'integration_test\\images\\IT_3.jpg'
img = cv2.imread(fname)
if _img_shape == None:
    _img_shape = img.shape[:2]
else:
    assert _img_shape == img.shape[:2], "All images must share the same size."
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# Find the chess board corners
ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH+cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)
# If found, add object points, image points (after refining them)
if ret == True:
    objpoints.append(objp)
    cv2.cornerSubPix(gray,corners,(3,3),(-1,-1),subpix_criteria)
    imgpoints.append(corners)
    
N_OK = len(objpoints)
K = np.zeros((3, 3))
D = np.zeros((4, 1))
rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
rms, K, D, rvecs, tvecs = \
    cv2.fisheye.calibrate(
        objpoints,
        imgpoints,
        gray.shape[::-1],
        K,
        D,
        rvecs,
        tvecs,
        calibration_flags,
        (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6)
    )
print("Found " + str(N_OK) + " valid images for calibration")
print("DIM=" + str(_img_shape[::-1]))
print("K=np.array(" + str(K.tolist()) + ")")
print("D=np.array(" + str(D.tolist()) + ")")
print("Rvec=np.array(" + str(rvecs) + ")")
print("tvec=np.array(" + str(tvecs) + ")")