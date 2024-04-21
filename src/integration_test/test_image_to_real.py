from catan_objects.TableComponents import CameraModule, Lights
from catan_objects.TableComponents import CameraRig
from integration_test.integration_setup import Setup
from catan_objects.BoardComponents import *
from catan_objects.Gantry import *

import numpy as np
import cv2

global_x, global_y = None, None

camera = CameraModule()
lights = Lights(1)
cam = CameraRig(camera, lights, position=[0,0])
cam.load_image('integration_test\\images\\homo00.jpg')
cam.undistort_picture()

pump_1 = PumpAssembly(Gate_Valve(GPIO_SETUP(6), GPIO_CONTROL_GATE, 6), DCMotor(HAT_SETUP("motor2", 0x62)), DCMotor(HAT_SETUP("motor1", 0x62)))
pump_2 = PumpAssembly(Gate_Valve(GPIO_SETUP(19), GPIO_CONTROL_GATE, 19), DCMotor(HAT_SETUP("motor4", 0x62)), DCMotor(HAT_SETUP("motor3", 0x62)))
# Since you only have one pump, need to switch
mount = Mount(Stepper(200, 40, HAT_SETUP('stepper1', 0x61), HAT_CONTROL), pump_2, pump_1)
catan_board = Setup((350,50))
gantry = Gantry(LinkedMotor(Stepper(200, 40, HAT_SETUP('stepper1')),
                Stepper(200, 40, HAT_SETUP('stepper2')), LINKED_HAT_CONTROL),
                mount, catan_board, [[0,100]], [[10,10], [20,10], [30,10]], [10,20],
                [10, 30], [10, 40], [10, 50], [10,60])

def on_mouse_click(event, x, y, flags, param):
    global global_x, global_y
    if event == cv2.EVENT_LBUTTONDOWN:
        global_x = x
        global_y = y
        cv2.destroyAllWindows()

cv2.namedWindow(winname = "Title of Popup Window") 
cv2.setMouseCallback("Title of Popup Window", on_mouse_click) 

while True: 
    cv2.imshow("Title of Popup Window", cam.image) 
      
    if cv2.waitKey(0): 
        break

coords = cam.convert_to_world_single(np.array([global_x, global_y]))
print(coords)

# number = Number(xy = [coords[0], coords[1]])
# gantry.catan_board.empty_spaces[0].push(number)

# # pick and place number
# gantry.pick_up(gantry.catan_board.empty_spaces[0])
# gantry.place(gantry.number_stacks)