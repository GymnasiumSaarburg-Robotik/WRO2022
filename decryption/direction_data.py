import re

from decryption.block import CCblock


class direction_data:

    def __init__(self, raw_data, current_direction):
        self.CONST_CAMERA_DIRECTION_WIDTH = 120  # TODO: Measure direction width
        self.CONST_CAMERA_PIXEL_WIDTH = 319  # Camera image is 319px

        self.rawData = raw_data
        self.blocks = []
        self.blockDirections = []
        self.current_direction = current_direction
        self.decrypt_data(current_direction)

    def decrypt_data(self, offset_direction):
        try:
            data = self.rawData
            data = re.findall('\[(.*?)\]', data)
            first = True
            for index, block in enumerate(data):
                if first:
                    block = block.replace("175, 193, 33, 42, 82, 7, ", "")
                block = block.replace("1, 0, ", "", 1)
                blockAsStringList = block.split(",")
                blockAsStringList = blockAsStringList[:-4]
                data = [int(x) for x in blockAsStringList]
                first = False
                summed_data = []
                num_hash = 0
                for i in range(len(data)):
                    num_hash += data[i]
                    if i % 2 != 0:
                        summed_data.append(num_hash)
                        num_hash = 0

                for i in range(1, int(len(summed_data) / 4) + 1):
                    base_index = i * 4 - 1
                    offset = 1000

                    x_center = offset + summed_data[base_index - 3]
                    y_center = summed_data[base_index - 2]
                    width = summed_data[base_index - 1]
                    height = summed_data[base_index]

                    direction = x_center / self.CONST_CAMERA_PIXEL_WIDTH * self.CONST_CAMERA_DIRECTION_WIDTH
                    direction -= offset_direction
                    if direction >= 359:
                        direction -= direction
                    print("Direction: " + str(direction))
                    block_object = CCblock(int(x_center), int(y_center), int(width * height), direction)
                    self.blocks.append(block_object)
        except True:  # Catch any exception
            print("Data could not be resolved.")
            return
        print("Generated direction data containing " + str(len(self.blocks)) + " blocks.")
