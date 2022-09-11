#!/usr/bin/env python3

# Old imports
import math
from time import sleep

from ev3dev2.motor import MediumMotor
from smbus import SMBus
from ev3dev2.display import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from ev3dev2.port import LegoPort
from ev3dev2.motor import *

from decryption.api2 import direction_data_new

from time import *

import ev3dev2.fonts as fonts

# New imports

display = Display()

c = GyroSensor(address=INPUT_3)
color = ColorSensor(address=INPUT_4)
c.reset()
print("init: " + str(c.angle))

def face_ramp(motor1, motor2, c):
    print("Facing ramp...")
    target = 0 # plus entspricht uhrzeigersinn, minus entgegen Uhrzeigersinn
    diff = target + c.angle # diff zwischen momentanem und target wert
    while diff > 3 or diff < -3:
        print(c.angle)
        diff = c.angle - target
        num = c.angle
        if (diff < 0) :
            motor1.on(10)
            motor2.on(-10)
        else :
            motor1.on(-10)
            motor2.on(10)
    motor1.off()
    motor2.off()

def only_contains_one_element(data):
    return len(set(data)) == 1

def shoot(motor1, motor2, shoot_motor, secure_motor):     
    blue = color.rgb[2]
    while (blue > 140):
        blue = color.rgb[2]
        if (c.angle > 0) :
            motor1.on(speed=90)
            motor2.on(speed=100)
        else :
            motor1.on(speed=90)
            motor2.on(speed=100)
    motor1.on_for_seconds(100, 0.5, False, False)
    motor2.on_for_seconds(100, 0.5, False, True)
    blue = color.rgb[2]
    while (blue > 200 or blue < 100):
        blue = color.rgb[2]
        if (c.angle > 0) :
            motor1.on(speed=45)
            motor2.on(speed=50)
        else :
            motor1.on(speed=45)
            motor2.on(speed=50)
    motor1.off()
    motor2.off()
    secure_motor.on_for_seconds(50, 2, False, True)
    shoot_motor.on_for_seconds(100, 0.5, False, True)

def move_towards_sleeping_pos1(motor1, motor2): # pos 1 describse the sleeping pos for a robot coming from shooting prcess
    motor1.on_for_seconds(100, 5, False, False)
    motor2.on_for_seconds(100, 5, False, True)


def readBlocks(address, bus, current_direction):
    # TODO: Move request packet into constant
    data = [174, 193, 32, 2, 255, 255]
    bus.write_i2c_block_data(address, 0, data)
    # Read first block
    data = ""
    block = bus.read_i2c_block_data(address, 0, 6 + 14)
    if not only_contains_one_element(block[7:]):
        data += str(block)
    while True:  # TODO: Test if ball count is accurate
        block2 = bus.read_i2c_block_data(address, 0, 14)
        if only_contains_one_element(block2):
            break
        data += "|\n" + str(block2)
    return direction_data_new(data, current_direction)


input1 = LegoPort(INPUT_1)
input1.mode = 'other-i2c'
sleep(0.5)
bus = SMBus(3)

chasingBall = False

address = 0x54

readBlocks(address, bus, 0)

motor1 = LargeMotor(OUTPUT_B)
motor2 = LargeMotor(OUTPUT_C)
motor_securing_balls = MediumMotor(OUTPUT_A)
shoot_motor = MediumMotor(OUTPUT_D)

while True:

    direction_data = readBlocks(address, bus, c.value())
    directions = direction_data.blockDirectionDiffs
    print("Count:" + str(len(directions)))
    directions = [round(num, 0) for num in directions]

    if len(directions) == 0:
        if chasingBall:
            motor1.on_for_seconds(20, 3, True, False)
            motor2.on_for_seconds(20, 3, True, False)
            sleep(1)
            motor_securing_balls.on_for_seconds(-15, 0.5, False, False)
            sleep(1)
            motor_securing_balls.off()  
            face_ramp(motor1, motor2, c)
            shoot(motor1, motor2, shoot_motor, motor_securing_balls)
            break
        else:
            motor1.off()
            motor2.off()
        continue

    targetDirection = directions[0]

    if 5 > targetDirection > -5:
        motor1.on(40, False, False)
        motor2.on(40, False, False)
        chasingBall = True
        continue

    motor1.on((targetDirection / 90) * 50, False, False)
    motor2.on((targetDirection / 90) * -50, False, False)

print("Done")
sleep(30)
