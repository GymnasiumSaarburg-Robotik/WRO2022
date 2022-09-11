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


motor1 = LargeMotor(OUTPUT_B)
motor2 = LargeMotor(OUTPUT_C)

display = Display()

color = ColorSensor(address=INPUT_4)
c = GyroSensor(address=INPUT_3)
