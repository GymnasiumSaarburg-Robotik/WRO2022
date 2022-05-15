#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks import *
from pybricks.iodevices import I2CDevice, Ev3devSensor
from pybricks.media.ev3dev import Font

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


def is_allowed_to_shoot(compass_value):
    return (compass_value > 20 and compass_value < 100)

def is_touching_line(colorvalue1, colorvalue2):
    return (colorvalue1 > 50 and colorvalue2 > 50)

def drive_main_motors(speed):
    main_motor_left = Motor(Port.B)
    main_motor_right = Motor(Port.C)
    main_motor_left.run(speed)
    main_motor_right.run(speed)

def stop_main_motors():
    main_motor_left = Motor(Port.B)
    main_motor_right = Motor(Port.C)
    main_motor_left.hold()
    main_motor_right.hold()

def turn_left(speed, speed_ratio):
    main_motor_left = Motor(Port.B)
    main_motor_right = Motor(Port.C)
    main_motor_left.run(speed * (-speed_ratio))
    main_motor_right.run(speed * speed_ratio)

def turn_right(speed, speed_ratio):
    main_motor_left = Motor(Port.B)
    main_motor_right = Motor(Port.C)
    main_motor_left.run(speed * speed_ratio)
    main_motor_right.run(speed * (-speed_ratio))

def custom_direction(raw_data):
    relevant_data = []
    relevant_data_divisor = 1
    for data_entry_index in range(len(raw_data)):
        data_entry = raw_data[data_entry_index]
        if data_entry > 1:
            relevant_data.append(data_entry_index * data_entry)
            relevant_data_divisor += data_entry
    print(relevant_data)
    relevant_data_sum = 0
    length = len(relevant_data)
    for relevant_data_entry in relevant_data:
        relevant_data_sum += relevant_data_entry
    return relevant_data_sum / relevant_data_divisor + 1



# Create your objects here.
ev3 = EV3Brick()
# drive_main_motors(360, 2000)
#colorsensor1 = ColorSensor(Port.S3)
#colorsensor2 = ColorSensor(Port.S4)
irseeker = Ev3devSensor(Port.S2)
compass = Ev3devSensor(Port.S1)
font = Font('Lucida', 15, False, False, None, None)
ev3.screen.set_font(font)
while True:

    direction = compass.read("COMPASS")[0]
    irseeker_values = irseeker.read("AC-ALL")
    max_irseeker_value = max(irseeker_values)
    rel_ball_position = 0

    #if is_touching_line(colorsensor1.reflection(), colorsensor2.reflection()):
    #    stop_main_motors()
    #    continue

    if max_irseeker_value > 10: # Avoid sensor noise
        #rel_ball_position = int(irseeker_values.index(max_irseeker_value))
        rel_ball_position = custom_direction(irseeker_values)

    
    shoot_motor = Motor(Port.D)
    if max_irseeker_value > 95 and is_allowed_to_shoot(direction):
        shoot_motor.run(2000)
    else:
        shoot_motor.hold()



    if rel_ball_position != 0 and max_irseeker_value < 115:
        if rel_ball_position < 3.5:
            pass
            turn_right(900, 0.5)
        elif rel_ball_position > 4.35:
            pass
            turn_left(900, 0.5)
        else:
            stop_main_motors()
    else:
        stop_main_motors()


    ev3.screen.clear()
    #ev3.screen.draw_text(0, 0, "Color value: 1" + str(colorsensor1.reflection()), text_color=Color.BLACK, background_color=None)
    #ev3.screen.draw_text(0, 25, "Color value: 2" + str(colorsensor2.reflection()), text_color=Color.BLACK, background_color=None)
    ev3.screen.draw_text(0, 50, "Max IR strength: " + str(max_irseeker_value), text_color=Color.BLACK, background_color=None)
    ev3.screen.draw_text(0, 75, "Compass: " + str(direction), text_color=Color.BLACK, background_color=None)
    wait(100)
    #direction = int(max(irseeker.read("AC-ALL")))
    #max_strength = int(max(irseeker.read("AC-ALL")))
    #if (max_strength < 120) :
    #    if (direction < 5 and direction != 0) :
    #        turn_right(100)
    #    elif (direction > 5 and direction != 0) :
    #        turn_left(100)
    #    else :
    #        drive_main_motors(100)
    #    wait(500)
    #else :
    #    drive_main_motors(500)
    #    wait(2000)

