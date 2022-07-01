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

from decryption.api import *

from time import *

import ev3dev2.fonts as fonts

# New imports

display = Display()

c = Sensor(address=INPUT_2, driver_name='ht-nxt-compass')
num = c.value()
print(num)


def readBlocks(address, bus, current_direction):
    # FIXME: Upper part should be constant

    # TODO: Move request packet into constant
    data = [174, 193, 32, 2, 255, 255]

    bus.write_i2c_block_data(address, 0, data)
    # Read first block
    data = ""
    block = bus.read_i2c_block_data(address, 0, 6 + 14)
    data += str(block)
    for index in range(0):  # TODO: Detect how many balls are found, currently hard coded to two
        block2 = bus.read_i2c_block_data(address, 0, 14)
        data += str(block2)
    print(data)
    return direction_data_new(data, current_direction)


input1 = LegoPort(INPUT_1)
input1.mode = 'other-i2c'
# Enabling the i2c port requires time
sleep(0.5)
# Settings for I2C (SMBus(3) for INPUT_1)
bus = SMBus(3)
address = 0x54


while True:
    direction_data = readBlocks(address, bus, c.value())
    directions = direction_data.blockDirections
    print("\n\n\n")
    print(str(directions))
    directions = [int(round(num, 0)) for num in directions]
    print(str(directions))


    targetDirection = directions[0]

    display.text_grid("Ball: " + str(directions[0]), True, 10, 3)
    display.text_grid("Kompass: " + str(c.value()), False, 10, 6)

    display.update()
    sleep(1)
