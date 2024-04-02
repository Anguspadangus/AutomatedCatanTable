from catan_objects.TableComponents import CameraModule, Lights
from catan_objects.TableComponents import CameraRig
import numpy as np
import cv2

camera = CameraModule()
lights = Lights(1)
cam = CameraRig(camera, lights, position=[0,0])
cam.load_image('integration_test\\images\\IT_2.jpg')
cam.undistort_picture()

xy = [[0,0], [250,50], [200,350], [50,350]]
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
    