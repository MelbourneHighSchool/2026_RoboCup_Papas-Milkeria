#!/usr/bin/env python3
from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_D, SpeedPercent
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sound import Sound
import time
sound = Sound()
tank = MoveTank(OUTPUT_D, OUTPUT_A)

leftcoloursensor = ColorSensor(INPUT_2)
rightcoloursensor = ColorSensor(INPUT_1)

leftcoloursensor.mode = "COL-REFLECT"
rightcoloursensor.mode = "COL-REFLECT"

LEFT_WHITE = 70
LEFT_BLACK = 10
RIGHT_WHITE = 70
RIGHT_BLACK = 10

MAX_BASE_SPEED = 30
MIN_BASE_SPEED = 12

KP = 32.0
KD = 1.8

SPEED_SLOWDOWN = 12.0
FILTER_ALPHA = 0.55
error_margin = 0.03

greenlowermarg = 15
greenuppermarg = 18
greenchecks = 2
greenleft = False
greemright = False

MAX_FORWARD = 50
MAX_REVERSE = 25

BOTH_DARK = 0.65

left_filtered = 0.0
right_filtered = 0.0
previous_error = 0.0
last_turn = 1

def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))

def darkness(reading, white, black):
    value = (white - reading) / (white - black)
    return clamp(value, 0.0, 1.0)

while True:
    left_raw = leftcoloursensor.reflected_light_intensity
    right_raw = rightcoloursensor.reflected_light_intensity
    if greenlowermarg < left_raw < greenuppermarg or greenlowermarg < right_raw < greenuppermarg:
        leftcoloursensor.mode = "COL-COLOR"
        rightcoloursensor.mode = "COL-COLOR"
        left_col = leftcoloursensor.color
        right_col = rightcoloursensor.color
        if left_col == 3:
            print("Left Green Seen")
        elif right_col == 3:
            print("Right Green Seen")
        elif right_col != 3 or left_col != 3:
            print("False alert nevermind continue")

    left_raw = leftcoloursensor.reflected_light_intensity
    right_raw = rightcoloursensor.reflected_light_intensity
    leftcoloursensor.mode = "COL-REFLECT"
    rightcoloursensor.mode = "COL-REFLECT"

    left_dark = darkness(left_raw, LEFT_WHITE, LEFT_BLACK)
    right_dark = darkness(right_raw, RIGHT_WHITE, RIGHT_BLACK)

    left_filtered = FILTER_ALPHA * left_dark + (1 - FILTER_ALPHA) * left_filtered
    right_filtered = FILTER_ALPHA * right_dark + (1 - FILTER_ALPHA) * right_filtered

    error = right_filtered - left_filtered

    if abs(error) < error_margin:
        error = 0.0

    if error < 0:
        last_turn = -1
    elif error > 0:
        last_turn = 1

    if left_filtered > BOTH_DARK and right_filtered > BOTH_DARK:
        error = last_turn

    derivative = error - previous_error
    previous_error = error

    correction = KP * error + KD * derivative

    base_speed = MAX_BASE_SPEED - SPEED_SLOWDOWN * abs(error)
    base_speed = clamp(base_speed, MIN_BASE_SPEED, MAX_BASE_SPEED)

    left_speed = base_speed + correction
    right_speed = base_speed - correction

    left_speed = clamp(left_speed, -MAX_REVERSE, MAX_FORWARD)
    right_speed = clamp(right_speed, -MAX_REVERSE, MAX_FORWARD)

    tank.on(
        SpeedPercent(left_speed),
        SpeedPercent(right_speed)
    )

    time.sleep(0.01)