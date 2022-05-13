#!/usr/bin/env python3
from time import sleep
from smbus import SMBus

from ev3dev2.display import Display
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.port import LegoPort

from ev3dev2.sound import Sound


def checkIfThereIsOnlyOneElement(arr):
    return arr[0] == arr[len(arr) - 1]


# EV3 Display
lcd = Display()

# Connect TouchSensor
touchsensor = TouchSensor(INPUT_4)

input1 = LegoPort(INPUT_1)
input1.mode = 'other-i2c'
# Enabling the i2c port requires time
sleep(0.5)

# Settings for I2C (SMBus(3) for INPUT_1)
bus = SMBus(3)
address = 0x54

data = [174, 193, 32, 2, 255, 255]

while not touchsensor.value():
    # Clear display
    lcd.clear()
    # Request block
    print("data: " + str(data))
    bus.write_i2c_block_data(address, 0, data)
    # Read block
    block = bus.read_i2c_block_data(address, 0, 6+14)
    print(str(block))
    for index in range(2):
        block2 = bus.read_i2c_block_data(address, 0, 14)
        print("Following block: " + str(block2))

    break
    # Extract data
    sig = block[7] * 256 + block[6]
    x = block[9] * 256 + block[8]
    y = block[11] * 256 + block[10]
    w = block[13] * 256 + block[12]
    h = block[15] * 256 + block[14]
    # Scale to resolution of EV3 display:
    # Resolution Pixy2 (316x208)
    # Resolution EV3 (178x128)
    x *= 0.6
    y *= 0.6
    w *= 0.6
    h *= 0.6
    # Calculate rectangle to draw on display
    dx = int(w / 2)
    dy = int(h / 2)
    xa = x - dx
    ya = y + dy
    xb = x + dx
    yb = y - dy
    lcd.draw.rectangle((xa, ya, xb, yb), fill='black')
    lcd.update()
