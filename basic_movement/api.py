import re

from constants.constants import constants
from decryption.block import CCblock


class basic_movement:

    def __init__(self):

        self.constants = constants()

        self.CONST_CAMERA_DIRECTION_WIDTH = 65  # Einstellen bezüglich Drehung
        self.CONST_CAMERA_PIXEL_WIDTH = 315  # Camera image is 319px

        self.rawData = raw_data
        self.blocks = []
        self.blockDirectionDiffs = []
        self.current_direction = current_direction
        self.decrypt_data(current_direction)

    def move_towards_sleeping_pos1(self, current_direction):
        pass


    def move_towards_sleeping_pos2(self, current_direction):
        pass