
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

K_init = np.array([[108.49354735654141, 0.0, 371.5786534104595], [0.0, 111.6060998517777, 205.3861581256824], [0.0, 0.0, 1.0]])
K = np.array([[0., 0.0, 0.], [0.0, 0., 0.], [0.0, 0.0, 1.0]])
D_init = np.array([[-1.1e-02], [ 8.0e-05], [ 3e-03], [-1.7e-03]], dtype=np.float64)
D = np.array([[0], [0], [0], [0]], dtype=np.float64)

cv.createTrackbar('K_00', 'Windows', 0, K_max, nothing)
cv.createTrackbar('K_02', 'Windows', 0, K_max, nothing)
cv.createTrackbar('K_11', 'Windows', 0, K_max, nothing)
cv.createTrackbar('K_12', 'Windows', 0, K_max, nothing)

cv.createTrackbar('D_0', 'Windows', 0, D_max, nothing)
cv.createTrackbar('D_1', 'Windows', 0, D_max, nothing)
cv.createTrackbar('D_2', 'Windows', 0, D_max, nothing)
cv.createTrackbar('D_3', 'Windows', 0, D_max, nothing)

cv.setTrackbarPos('K_00', 'Windows', int(K_max/2))
cv.setTrackbarPos('K_02', 'Windows', int(K_max/2))
cv.setTrackbarPos('K_11', 'Windows', int(K_max/2))
cv.setTrackbarPos('K_12', 'Windows', int(K_max/2))

cv.setTrackbarPos('D_0', 'Windows', int(D_max/2))
cv.setTrackbarPos('D_1', 'Windows', int(D_max/2))
cv.setTrackbarPos('D_2', 'Windows', int(D_max/2))
cv.setTrackbarPos('D_3', 'Windows', int(D_max/2))

while True:
    frame = cv.imread('integration_test\\images\\IT_2.jpg')

    K[0][0] = K_init[0][0] + (cv.getTrackbarPos('K_00', 'Windows') - K_max/2) / K_scalar
    K[0][2] = K_init[0][2] + (cv.getTrackbarPos('K_02', 'Windows') - K_max/2) / K_scalar
    K[1][1] = K_init[1][1] + (cv.getTrackbarPos('K_11', 'Windows') - K_max/2) / K_scalar
    K[1][2] = K_init[1][2] + (cv.getTrackbarPos('K_12', 'Windows') - K_max/2) / K_scalar

    D[0] = D_init[0] + (cv.getTrackbarPos('D_0', 'Windows') - D_max/2) / D_scaler_1
    D[1] = D_init[1] + (cv.getTrackbarPos('D_1', 'Windows') - D_max/2) / D_scaler_3
    D[2] = D_init[2] + (cv.getTrackbarPos('D_2', 'Windows') - D_max/2) / D_scaler_2
    D[3] = D_init[3] + (cv.getTrackbarPos('D_3', 'Windows') - D_max/2) / D_scaler_2
    
    h, w = frame.shape[:2]
    new_camera_matrix, roi = cv.getOptimalNewCameraMatrix(K, D, (w, h), 1, (w, h))
    frame = cv.undistort(frame, K, D, newCameraMatrix=new_camera_matrix)
    cv.imshow('frame', frame)

    key = cv.waitKey(1)
    if key == ord('q'):
        break
cv.destroyAllWindows()
print(K)
print(D)
