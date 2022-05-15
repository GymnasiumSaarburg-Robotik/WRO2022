#!/usr/bin/env python3

# Old imports
from time import sleep
from smbus import SMBus
from ev3dev2.display import Display
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.port import LegoPort
from ev3dev2.sound import Sound

# New imports
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks import *
from pybricks.iodevices import I2CDevice, Ev3devSensor
from pybricks.media.ev3dev import Font

ev3 = EV3Brick()
compass = Ev3devSensor(Port.S1)

font = Font('Lucida', 15, False, False, None, None)
ev3.screen.set_font(font)

while True:
    direction = compass.read("COMPASS")[0]
    ev3.screen.clear()
    ev3.screen.draw_text(0, 75, "Compass: " + str(direction), text_color=Color.BLACK, background_color=None)
    wait(100)
