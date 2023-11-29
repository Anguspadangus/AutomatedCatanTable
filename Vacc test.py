# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 13:44:26 2023

@author: Owen Porpora
"""

from adafruit_motor import motor
from adafruit_motorkit import MotorKit
import time

# Create the motor kit object
kit = MotorKit()

def run_motor(throttle, duration):
    kit.motor_M3.throttle = throttle
    time.sleep(duration)
    kit.motor_M3.throttle = 0

try:
    # Blow out air at half throttle for 1 second
    run_motor(-0.5, 1)

    # Suck in air at full throttle for 5 seconds
    run_motor(1, 5)

finally:
    # Turn off the motor
    kit.motor_M3.throttle = 0
