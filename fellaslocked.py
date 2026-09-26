#!/usr/bin/env python3
"""
Full black sub 10
Black Generally Say seen at sub 15 that's half in half out
little black can go all the way to 60
Say white is 93+
"""
from ev3dev2.motor import OUTPUT_D, OUTPUT_A, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import ColorSensor
import time


tank = MoveTank(OUTPUT_D, OUTPUT_A)

leftsensor = ColorSensor(INPUT_2)
rightsensor = ColorSensor(INPUT_1)

leftsensor.mode = "COL-REFLECT"
rightsensor.mode = "COL-REFLECT"

speed = 20
white = 90
black = 15

while True:
    leftreflectivity = leftsensor.reflected_light_intensity
    rightreflectivity = rightsensor.reflected_light_intensity
    