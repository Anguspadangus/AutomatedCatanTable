from catan_objects.TableComponents import CameraModuleCatan, Lights
from catan_objects.TableComponents import CameraRig
import numpy as np
import cv2

camera = CameraModuleCatan()

cam = CameraRig(camera, None, position=[0,0])
cam.load_image('/home/pi/Desktop/cam/homo_1.jpg')
cam.undistort_picture()

xy = []
for i in range(int(200/50)):
    for j in range(int(400/50)):
        if i == 100 and j == 350:
            continue
        elif i == 150 and j == 350:
            continue
        else:
            xy.append([i*50, j*50])
uv = []

def on_mouse_click(event, x, y, flags, param):
    global uv, xy
    if event == cv2.EVENT_LBUTTONDOWN:
        uv.append([x, y])
        cv2.circle(cam.image, (x,y), 5, color=(255, 0, 0),thickness=2)
        cv2.imshow('Test', cam.image)
        
        if len(uv) != len(xy):
            print(f'Select {xy[len(uv)]}')
        
cv2.namedWindow(winname = "Test") 
cv2.setMouseCallback("Test", on_mouse_click) 
cv2.imshow('Test', cam.image)

print(f'Select {xy[0]}')

while len(uv) < len(xy):
    cv2.waitKey(1)

cv2.destroyAllWindows()
    
h, status = cv2.findHomography(np.array(xy), np.array(uv))
print(h)
    