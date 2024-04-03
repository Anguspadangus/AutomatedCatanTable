
import numpy as np
import cv2 as cv

K_max = 100
D_max = 100

K_scalar = 10
D_scaler_1 = 2000
D_scaler_2 = 10000
D_scaler_3 = 1000000
def nothing(x):
    pass

cv.namedWindow('Windows')

# K_init = np.array([[178.37412288,0.,337.56981617], [ 0., 178.35548935, 234.22585533], [ 0., 0., 1., ]])
K_init = np.array([[324.76825238, 0. ,373.66404696], [0., 326.72841161, 247.07466765], [0., 0., 1., ]])
K = np.array([[0., 0.0, 0.], [0.0, 0., 0.], [0.0, 0.0, 1.0]])
# D_init = np.array([[-5.0e-02],
#  [ 2.0e-06],
#  [ 4.0e-03],
#  [ 1.5e-03]])
D_init = np.array([[-0.31685422,  0.11733933, -0.00043777,  0.00120568, -0.02182481]])

D = np.array([[0, 0, 0, 0, 0]], dtype=np.float64)

cv.createTrackbar('K_00', 'Windows', 0, K_max, nothing)
cv.createTrackbar('K_02', 'Windows', 0, K_max, nothing)
cv.createTrackbar('K_11', 'Windows', 0, K_max, nothing)
cv.createTrackbar('K_12', 'Windows', 0, K_max, nothing)

cv.createTrackbar('D_0', 'Windows', 0, D_max, nothing)
cv.createTrackbar('D_1', 'Windows', 0, D_max, nothing)
cv.createTrackbar('D_2', 'Windows', 0, D_max, nothing)
cv.createTrackbar('D_3', 'Windows', 0, D_max, nothing)
cv.createTrackbar('D_4', 'Windows', 0, D_max, nothing)

cv.setTrackbarPos('K_00', 'Windows', int(K_max/2))
cv.setTrackbarPos('K_02', 'Windows', int(K_max/2))
cv.setTrackbarPos('K_11', 'Windows', int(K_max/2))
cv.setTrackbarPos('K_12', 'Windows', int(K_max/2))

cv.setTrackbarPos('D_0', 'Windows', int(D_max/2))
cv.setTrackbarPos('D_1', 'Windows', int(D_max/2))
cv.setTrackbarPos('D_2', 'Windows', int(D_max/2))
cv.setTrackbarPos('D_3', 'Windows', int(D_max/2))
cv.setTrackbarPos('D_4', 'Windows', int(D_max/2))

while True:
    frame = cv.imread('integration_test\\images\\homo01.jpg')

    K[0][0] = K_init[0][0] + (cv.getTrackbarPos('K_00', 'Windows') - K_max/2) / K_scalar
    K[0][2] = K_init[0][2] + (cv.getTrackbarPos('K_02', 'Windows') - K_max/2) / K_scalar
    K[1][1] = K_init[1][1] + (cv.getTrackbarPos('K_11', 'Windows') - K_max/2) / K_scalar
    K[1][2] = K_init[1][2] + (cv.getTrackbarPos('K_12', 'Windows') - K_max/2) / K_scalar

    D[0][0] = D_init[0][0] + (cv.getTrackbarPos('D_0', 'Windows') - D_max/2) / D_scaler_1
    D[0][1] = D_init[0][1] + (cv.getTrackbarPos('D_1', 'Windows') - D_max/2) / D_scaler_3
    D[0][2] = D_init[0][2] + (cv.getTrackbarPos('D_2', 'Windows') - D_max/2) / D_scaler_2
    D[0][3] = D_init[0][3] + (cv.getTrackbarPos('D_3', 'Windows') - D_max/2) / D_scaler_2
    D[0][4] = D_init[0][4] + (cv.getTrackbarPos('D_4', 'Windows') - D_max/2) / D_scaler_2
    
    h, w = frame.shape[:2]
    new_camera_matrix, roi = cv.getOptimalNewCameraMatrix(K, D, (w,h), 0, (w,h))
    frame = cv.undistort(frame, K, D, newCameraMatrix=new_camera_matrix)
    cv.imshow('frame', frame)

    key = cv.waitKey(1)
    if key == ord('q'):
        break
cv.destroyAllWindows()
print(K)
print(D)
