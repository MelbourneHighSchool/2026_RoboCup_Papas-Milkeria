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


WHITE_THRESHOLD = 70
WHITE_CONFIRMATIONS = 2

FORWARD_SPEED = 25
TURN_SPEED = 12
SHARP_TURN_SPEED = 18
REVERSE_SPEED = 8
SHARP_REVERSE_SPEED = 14


GREEN_REFLECT_MIN = 15
GREEN_REFLECT_MAX = 30

GREEN_CONFIRMATIONS = 2
GREEN_CHECK_DELAY = 0.05
GREEN_COOLDOWN = 1.0

GREEN_FORWARD_SPEED = 12
GREEN_FORWARD_TIME = 0.35

GREEN_TURN_SPEED = 18
GREEN_TURN_TIME = 0.65


last_turn = 1
white_count = 0
green_cooldown_until = 0.0


def check_green():
    tank.stop()

    leftcoloursensor.mode = "COL-COLOR"
    rightcoloursensor.mode = "COL-COLOR"

    time.sleep(GREEN_CHECK_DELAY)

    left_green_count = 0
    right_green_count = 0

    for _ in range(3):
        if leftcoloursensor.color == ColorSensor.COLOR_GREEN:
            left_green_count += 1

        if rightcoloursensor.color == ColorSensor.COLOR_GREEN:
            right_green_count += 1

        time.sleep(0.02)

    leftcoloursensor.mode = "COL-REFLECT"
    rightcoloursensor.mode = "COL-REFLECT"

    time.sleep(GREEN_CHECK_DELAY)

    left_green = left_green_count >= GREEN_CONFIRMATIONS
    right_green = right_green_count >= GREEN_CONFIRMATIONS

    if left_green and right_green:
        return "both"

    if left_green:
        return "left"

    if right_green:
        return "right"

    return None


def execute_green_turn(direction):
    tank.stop()

    tank.on_for_seconds(
        SpeedPercent(GREEN_FORWARD_SPEED),
        SpeedPercent(GREEN_FORWARD_SPEED),
        GREEN_FORWARD_TIME
    )

    if direction == "left":
        tank.on_for_seconds(
            SpeedPercent(-GREEN_TURN_SPEED),
            SpeedPercent(GREEN_TURN_SPEED),
            GREEN_TURN_TIME
        )

    elif direction == "right":
        tank.on_for_seconds(
            SpeedPercent(GREEN_TURN_SPEED),
            SpeedPercent(-GREEN_TURN_SPEED),
            GREEN_TURN_TIME
        )

    elif direction == "both":
        tank.on_for_seconds(
            SpeedPercent(GREEN_TURN_SPEED),
            SpeedPercent(-GREEN_TURN_SPEED),
            GREEN_TURN_TIME * 2
        )

    tank.stop()


try:
    while True:
        left = leftcoloursensor.reflected_light_intensity
        right = rightcoloursensor.reflected_light_intensity

        current_time = time.monotonic()

        left_possible_green = (
            GREEN_REFLECT_MIN <= left <= GREEN_REFLECT_MAX
        )

        right_possible_green = (
            GREEN_REFLECT_MIN <= right <= GREEN_REFLECT_MAX
        )

        if (
            current_time >= green_cooldown_until
            and (left_possible_green or right_possible_green)
        ):
            green_direction = check_green()

            if green_direction is not None:
                execute_green_turn(green_direction)

                green_cooldown_until = (
                    time.monotonic() + GREEN_COOLDOWN
                )

                white_count = 0
                continue

        left_white = left >= WHITE_THRESHOLD
        right_white = right >= WHITE_THRESHOLD

        if left_white and right_white:
            white_count += 1

            if white_count >= WHITE_CONFIRMATIONS:
                tank.on(
                    SpeedPercent(FORWARD_SPEED),
                    SpeedPercent(FORWARD_SPEED)
                )
            else:
                tank.stop()

        elif not left_white and right_white:
            white_count = 0
            last_turn = -1

            if left < WHITE_THRESHOLD - 15:
                tank.on(
                    SpeedPercent(-SHARP_REVERSE_SPEED),
                    SpeedPercent(SHARP_TURN_SPEED)
                )
            else:
                tank.on(
                    SpeedPercent(-REVERSE_SPEED),
                    SpeedPercent(TURN_SPEED)
                )

        elif left_white and not right_white:
            white_count = 0
            last_turn = 1

            if right < WHITE_THRESHOLD - 15:
                tank.on(
                    SpeedPercent(SHARP_TURN_SPEED),
                    SpeedPercent(-SHARP_REVERSE_SPEED)
                )
            else:
                tank.on(
                    SpeedPercent(TURN_SPEED),
                    SpeedPercent(-REVERSE_SPEED)
                )

        else:
            white_count = 0

            if last_turn == -1:
                tank.on(
                    SpeedPercent(-REVERSE_SPEED),
                    SpeedPercent(REVERSE_SPEED)
                )
            else:
                tank.on(
                    SpeedPercent(REVERSE_SPEED),
                    SpeedPercent(-REVERSE_SPEED)
                )

        time.sleep(0.01)

finally:
    tank.stop()