import re

s = '[175, 193, 33, 42, 82, 7, 1, 0, 252, 0, 191, 0, 36, 0, 29, 0, 0, 0, 2, 255]' \
    '[1, 0, 118, 0, 165, 0, 28, 0, 24, 0, 0, 0, 3, 255]' \
    '[1, 0, 6, 0, 22, 0, 12, 0, 18, 0, 0, 0, 200, 255]'
blocksAsStringList = re.findall('\[(.*?)\]', s)

first = True
for block in blocksAsStringList:
    if first:
        block = block.replace("175, 193, 33, 42, 82, 7, ", "")
    block = block.replace("1, 0, ", "", 1)
    blockAsStringList = block.split(",")
    blockAsStringList = blockAsStringList[:-4]
    data = [int(x) for x in blockAsStringList]
    print(data)
    first = False