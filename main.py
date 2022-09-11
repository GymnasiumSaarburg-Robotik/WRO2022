#!/usr/bin/env python3

from smbus import SMBus
from ev3dev2.display import *
from ev3dev2.sensor import *
from ev3dev2.port import LegoPort
from ev3dev2.motor import *

from decryption.api import direction_data_new

from time import *

from constants.constants import constants
from basic_movement.api import basic_movement


def face_ramp():
    print("Facing ramp...")
    target = 0  # plus entspricht uhrzeigersinn, minus entgegen Uhrzeigersinn
    diff = target + c.GYRO_SENSOR.angle  # diff zwischen momentanem und target wert
    while diff > 3 or diff < -3:
        print(c.GYRO_SENSOR.angle)
        diff = c.GYRO_SENSOR.angle - target
        if diff < 0:
            c.DRIVING_MOTOR_LEFT.on(10)
            c.DRIVING_MOTOR_RIGHT.on(-10)
        else:
            c.DRIVING_MOTOR_LEFT.on(-10)
            c.DRIVING_MOTOR_RIGHT.on(10)
    c.DRIVING_MOTOR_LEFT.off()
    c.DRIVING_MOTOR_RIGHT.off()


def only_contains_one_element(data):
    return len(set(data)) == 1


def shoot():
    blue = c.COLOR_SENSOR.rgb[2]
    while blue > 140:
        blue = c.COLOR_SENSOR.rgb[2]
        if c.GYRO_SENSOR.angle > 0:
            c.DRIVING_MOTOR_LEFT.on(speed=90)
            c.DRIVING_MOTOR_RIGHT.on(speed=100)
        else:
            c.DRIVING_MOTOR_LEFT.on(speed=90)
            c.DRIVING_MOTOR_RIGHT.on(speed=100)
    c.DRIVING_MOTOR_LEFT.on_for_seconds(100, 0.5, False, False)
    c.DRIVING_MOTOR_RIGHT.on_for_seconds(100, 0.5, False, True)
    blue = c.COLOR_SENSOR.rgb[2]
    while blue > 200 or blue < 100:
        blue = c.COLOR_SENSOR.rgb[2]
        if c.GYRO_SENSOR.angle > 0:
            c.DRIVING_MOTOR_LEFT.on(speed=45)
            c.DRIVING_MOTOR_RIGHT.on(speed=50)
        else:
            c.DRIVING_MOTOR_LEFT.on(speed=45)
            c.DRIVING_MOTOR_RIGHT.on(speed=50)
    c.DRIVING_MOTOR_LEFT.off()
    c.DRIVING_MOTOR_RIGHT.off()
    c.SECURING_MOTOR.on_for_seconds(50, 2, False, True)
    c.SHOOTING_MOTOR.on_for_seconds(100, 0.5, False, True)


def move_towards_sleeping_pos1():  # pos 1 describse the sleeping pos for a robot coming from shooting process
    c.DRIVING_MOTOR_LEFT.on_for_seconds(100, 5, False, False)
    c.DRIVING_MOTOR_RIGHT.on_for_seconds(100, 5, False, True)


def readBlocks(current_direction):
    data = [174, 193, 32, 2, 255, 255]
    c.BUS.write_i2c_block_data(c.CAMERA_ADDRESS, 0, data)
    # Read first block
    data = ""
    block = c.BUS.read_i2c_block_data(c.CAMERA_ADDRESS, 0, 6 + 14)
    if not only_contains_one_element(block[7:]):
        data += str(block)
    while True:
        block2 = c.BUS.read_i2c_block_data(c.CAMERA_ADDRESS, 0, 14)
        if only_contains_one_element(block2):
            break
        data += "|\n" + str(block2)
    return direction_data_new(data, current_direction)


c = constants()
bm = basic_movement(c)

c.GYRO_SENSOR.reset()
print("init: " + str(c.GYRO_SENSOR.angle))
chasingBall = False

while True:
    direction_data = readBlocks(c.GYRO_SENSOR.value())
    directions = direction_data.blockDirectionDiffs
    print("Count:" + str(len(directions)))
    directions = [round(num, 0) for num in directions]

    if len(directions) == 0:
        if chasingBall:
            c.DRIVING_MOTOR_LEFT.on_for_seconds(20, 3, True, False)
            c.DRIVING_MOTOR_RIGHT.on_for_seconds(20, 3, True, False)
            sleep(1)
            c.SECURING_MOTOR.on_for_seconds(-15, 0.5, False, False)
            sleep(1)
            c.SECURING_MOTOR.off()
            face_ramp()
            shoot()
            break
        else:
            c.DRIVING_MOTOR_LEFT.off()
            c.DRIVING_MOTOR_RIGHT.off()
        continue

    targetDirection = directions[0]

    if 5 > targetDirection > -5:
        c.DRIVING_MOTOR_LEFT.on(40, False, False)
        c.DRIVING_MOTOR_RIGHT.on(40, False, False)
        chasingBall = True
        continue

    c.DRIVING_MOTOR_LEFT.on((targetDirection / 90) * 50, False, False)
    c.DRIVING_MOTOR_RIGHT.on((targetDirection / 90) * -50, False, False)

print("Done")
sleep(30)
