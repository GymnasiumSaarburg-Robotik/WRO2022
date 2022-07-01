import re

from decryption.block import CCblock


class direction_data_new:

    def __init__(self, raw_data, current_direction):
        self.CONST_CAMERA_DIRECTION_WIDTH = 65  # Einstellen bezüglich Drehung
        self.CONST_CAMERA_PIXEL_WIDTH = 315  # Camera image is 319px

        self.rawData = raw_data
        self.blocks = []
        self.blockDirections = []
        self.current_direction = current_direction
        self.decrypt_data(current_direction)

    def decrypt_data(self, current_direction):
        try:
            data = self.rawData
            data = re.findall('\[(.*?)\]', data)
            first = True
            for index, block in enumerate(data):
                block = block.replace("1, 0, ", "", 1)
                block_as_string_list = block.split(",")
                if first:
                    block_as_string_list = block_as_string_list[5:]
                    first = False
                block_as_string_list = block_as_string_list[:-4]
                data = [int(x) for x in block_as_string_list]
                summed_data = []
                num_hash = 0
                for i in range(len(data)):
                    num_hash += data[i]
                    if i % 2 != 0:
                        summed_data.append(num_hash)
                        num_hash = 0

                for i in range(1, int(len(summed_data) / 4) + 1):
                    base_index = i * 4 - 1

                    x_center = summed_data[base_index - 3]
                    y_center = summed_data[base_index - 2]
                    width = summed_data[base_index - 1]
                    height = summed_data[base_index]

                    # Relative Position im Bild [<0.5; 0.5; >0.5]
                    relative_direction = x_center / self.CONST_CAMERA_PIXEL_WIDTH
                    direction = current_direction
                    if relative_direction > 0.5:
                        relative_direction -= 0.5
                        direction_offset = relative_direction * self.CONST_CAMERA_DIRECTION_WIDTH
                        direction += direction_offset
                        print(direction_offset)
                    elif relative_direction < 0.5:
                        relative_direction = 0.5 - relative_direction
                        direction_offset = relative_direction * self.CONST_CAMERA_DIRECTION_WIDTH
                        direction -= direction_offset
                        print(direction_offset)

                    if direction >= 359:
                        direction -= 359
                    if direction < 0:
                        direction += 359
                    print("Direction: " + str(direction))
                    block_object = CCblock(int(x_center), int(y_center), int(width * height), direction)
                    self.blocks.append(block_object)
                    self.blockDirections.append(direction)
        except True:  # Catch any exception
            print("Data could not be resolved.")
            return
        print("Generated direction data containing " + str(len(self.blocks)) + " blocks.")
