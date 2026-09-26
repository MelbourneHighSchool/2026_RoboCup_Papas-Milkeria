#!/usr/bin/env python3

from ev3dev2.motor import OUTPUT_D, OUTPUT_A, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_2, INPUT_1
from ev3dev2.sensor.lego import ColorSensor
import time


left_motor_port = OUTPUT_D
right_motor_port = OUTPUT_A

left_sensor = ColorSensor(INPUT_2)
right_sensor = ColorSensor(INPUT_1)

left_sensor.mode = "COL-REFLECT"
right_sensor.mode = "COL-REFLECT"

tank = MoveTank(left_motor_port, right_motor_port)


BASE_SPEED = 20
TURN_STRENGTH = 12
BLACK_THRESHOLD = 35
CONTROL_PERIOD = 0.02


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


try:
    while True:
        left_reflect = left_sensor.reflected_light_intensity
        right_reflect = right_sensor.reflected_light_intensity

        left_black = left_reflect < BLACK_THRESHOLD
        right_black = right_reflect < BLACK_THRESHOLD

        if left_black and not right_black:
            left_speed = BASE_SPEED - TURN_STRENGTH
            right_speed = BASE_SPEED + TURN_STRENGTH

        elif right_black and not left_black:
            left_speed = BASE_SPEED + TURN_STRENGTH
            right_speed = BASE_SPEED - TURN_STRENGTH

        elif left_black and right_black:
            left_speed = BASE_SPEED * 0.5
            right_speed = BASE_SPEED * 0.5

        else:
            left_speed = BASE_SPEED
            right_speed = BASE_SPEED

        left_speed = clamp(left_speed, -50, 50)
        right_speed = clamp(right_speed, -50, 50)

        tank.on(
            SpeedPercent(left_speed),
            SpeedPercent(right_speed)
        )

        time.sleep(CONTROL_PERIOD)

except KeyboardInterrupt:
    tank.stop()