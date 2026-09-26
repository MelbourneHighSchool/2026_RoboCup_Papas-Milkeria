#!/usr/bin/env python3
from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_D, SpeedPercent
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_1, INPUT_2
import time

tank = MoveTank(OUTPUT_D, OUTPUT_A)

leftcoloursensor = ColorSensor(INPUT_2)
rightcoloursensor = ColorSensor(INPUT_1)

leftcoloursensor.mode = "COL-REFLECT"
rightcoloursensor.mode = "COL-REFLECT"

BASE_SPEED = 25
TURN_SPEED = 15
REVERSE_SPEED = 10
BLACK_THRESHOLD = 20

while True:
    left = leftcoloursensor.reflected_light_intensity
    right = rightcoloursensor.reflected_light_intensity

    if left > BLACK_THRESHOLD and right > BLACK_THRESHOLD:
        tank.on(SpeedPercent(BASE_SPEED), SpeedPercent(BASE_SPEED))

    elif left <= BLACK_THRESHOLD and right > BLACK_THRESHOLD:
        tank.on(SpeedPercent(-REVERSE_SPEED), SpeedPercent(TURN_SPEED))

    elif right <= BLACK_THRESHOLD and left > BLACK_THRESHOLD:
        tank.on(SpeedPercent(TURN_SPEED), SpeedPercent(-REVERSE_SPEED))

    else:
        tank.on(SpeedPercent(-REVERSE_SPEED), SpeedPercent(REVERSE_SPEED))

    time.sleep(0.01)