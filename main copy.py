#!/usr/bin/env python3

# Old imports
import math
from time import sleep

from ev3dev2.motor import MediumMotor
from smbus import SMBus
from ev3dev2.display import *
from ev3dev2.sensor import *
from ev3dev2.port import LegoPort
from ev3dev2.motor import *

from decryption.api2 import direction_data_new

from time import *

import ev3dev2.fonts as fonts

# New imports

display = Display()

c = Sensor(address=INPUT_2, driver_name='ht-nxt-compass')
num = c.value()
print(num)


def only_contains_one_element(data):
    return len(set(data)) == 1


def readBlocks(address, bus, current_direction):
    # FIXME: Upper part should be constant

    # TODO: Move request packet into constant
    data = [174, 193, 32, 2, 255, 255]

    bus.write_i2c_block_data(address, 0, data)
    # Read first block
    data = ""
    block = bus.read_i2c_block_data(address, 0, 6 + 14)
    if not only_contains_one_element(block[7:]):
        data += str(block)
    while True:  # TODO: Add max iterations
        block2 = bus.read_i2c_block_data(address, 0, 14)
        if only_contains_one_element(block2):
            break
        data += "|\n" + str(block2)

    print(data)
    return direction_data_new(data, current_direction)


input1 = LegoPort(INPUT_1)
input1.mode = 'other-i2c'
# Enabling the i2c port requires time
sleep(0.5)
# Settings for I2C (SMBus(3) for INPUT_1)
bus = SMBus(3)

chasingBall = False

address = 0x54

readBlocks(address, bus, 0)

motor1 = LargeMotor(OUTPUT_B)
motor2 = LargeMotor(OUTPUT_C)

while True:

    direction_data = readBlocks(address, bus, c.value())
    directions = direction_data.blockDirectionDiffs
    directions = [round(num, 0) for num in directions]

    if len(directions) == 0:
        if chasingBall:
            motor1.on_for_seconds(15, 3, True, False)
            motor2.on_for_seconds(15, 3, True, True)
            chasingBall = False
        else:
            motor1.off()
            motor2.off()
        continue

    targetDirection = directions[0]

    if 5 > targetDirection > -5:
        motor1.on(70, False, False)
        motor2.on(70, False, False)
        chasingBall = True
        continue

    motor1.on((targetDirection / 90) * 100, False, False)
    motor2.on((targetDirection / 90) * -100, False, False)
