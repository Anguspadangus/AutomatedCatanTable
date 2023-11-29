# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 00:46:18 2023

@author: Owen Porpora
"""

import time
from adafruit_motorkit import MotorKit

# Initialize the motor kit
kit = MotorKit()

# Define home positions for each color
HOME_POSITIONS = {
    'blue': (blue_home_x, blue_home_y),
    'red': (red_home_x, red_home_y),
    'white': (white_home_x, white_home_y),
    'orange': (orange_home_x, orange_home_y),
}

# Current position of the gantry
current_position = {'x': 0, 'y': 0}

# Define the steps per revolution for your stepper motors
STEPS_PER_REV = 200  # Adjust this based on your stepper motor specifications

# Define the maximum speed for your motors (steps per second)
MAX_SPEED = 400

# Define home and pick positions for the gripper
GRIPPER_HOME_POSITION = 0  # Replace with the actual home position
GRIPPER_PICK_POSITION = 180  # Replace with the actual pick position

class GamePiece:
    def __init__(self, name, height, weight, z_pick, z_target):
        self.name = name
        self.height = height
        self.weight = weight
        self.z_pick = z_pick
        self.z_target = z_target

    def get_count(self):
        # Placeholder method to get the count of the game piece
        # You should replace this with the actual logic
        return 0

class Road(GamePiece):
    def __init__(self):
        super().__init__('road', 1, 1, 1, 1)  

class Settlement(GamePiece):
    def __init__(self):
        super().__init__('settlement', 1, 1, 1, 1)

class City(GamePiece):
    def __init__(self):
        super().__init__('city', 1, 1, 1, 1)

class Number(GamePiece):
    def __init__(self):
        super().__init__('number', 1, 1, 1, 1)

class Hexagon(GamePiece):
    def __init__(self):
        super().__init__('hexagon', 1, 1, 1, 1)

class Robber(GamePiece):
    def __init__(self):
        super().__init__('robber', 1, 1, 1, 1)


# Function to move to a specific (x, y) coordinate
def move_to(x, y):
    global current_position

    # Calculate the relative movement required for both X and Y axes
    x_distance = x - current_position['x']
    y_distance = y - current_position['y']

    # Calculate the number of steps required for both X and Y axes
    x_steps = int(x_distance * (STEPS_PER_REV / 360))
    y_steps = int(y_distance * (STEPS_PER_REV / 360))

    # Set the speed for both motors
    kit.stepper1.setMaxSpeed(MAX_SPEED)
    kit.stepper2.setMaxSpeed(MAX_SPEED)

    # Move both X and Y motors simultaneously
    kit.stepper1.step(x_steps, direction=1 if x_distance > 0 else -1, style=2)
    kit.stepper2.step(y_steps, direction=1 if y_distance > 0 else -1, style=2)

    # Update the current position
    current_position['x'] = x
    current_position['y'] = y

    # Wait for both motors to complete their movements
    while kit.stepper1.isBusy() or kit.stepper2.isBusy():
        time.sleep(0.1)

# Function to move the gripper up and down
def move_gripper(direction):
    global GRIPPER_HOME_POSITION, GRIPPER_PICK_POSITION

    # Determine the target position based on the direction
    target_position = GRIPPER_HOME_POSITION if direction == 'home' else GRIPPER_PICK_POSITION

    # Calculate the number of steps required
    steps = int((target_position / 360) * STEPS_PER_REV)

    # Set the speed for the gripper motor
    kit.stepper3.setMaxSpeed(MAX_SPEED)  # Adjust this based on your stepper motor specifications

    # Move the gripper motor to the target position
    kit.stepper3.step(steps, direction=1 if target_position > 0 else -1, style=2)

    # Wait for the motor to complete its movement
    while kit.stepper3.isBusy():
        time.sleep(0.1)

# Function to pick up an object at a given (x, y) coordinate
def pick_up(x, y):
    move_to(x, y)
    move_gripper("pick")  # Move the gripper to the pick position

    # Turn on the DC motor
    kit.motor1.throttle = 1.0

    # Wait for three seconds
    time.sleep(3)

    # Move the gripper back to the home position
    move_gripper("home")

# Function to place the object at a target (x, y) coordinate
def place_object(x, y, color):
    move_to(x, y)
    move_gripper("pick")  # Move the gripper to the up position

    # Turn off the DC motor
    kit.motor1.throttle = 0

    # Move the gripper back to the home position for the specified color
    home_position = HOME_POSITIONS[color]
    move_to(home_position[0], home_position[1])
    move_gripper("home")

# Higher-level function for pick-and-place operation
def pick_and_place(color, x_coords, y_coords):
    for x, y in zip(x_coords, y_coords):
        move_to(x, y)
        pick_up(x, y)
        place_object(x, y, color)

# Example usage
blue_x_coords = [x1, x2, ...]
blue_y_coords = [y1, y2, ...]
# Repeat for other colors

# Perform pick-and-place for each color
pick_and_place('blue', blue_x_coords, blue_y_coords)
# Repeat for other colors

