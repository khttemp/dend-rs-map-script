import struct
import os
import sys

def readBinary(line, mode):
    if mode == "short":
        s = struct.unpack("<h", line)[0]
        return s
    elif mode == "ushort":
        s = struct.unpack("<H", line)[0]
        return s
    elif mode == "int":
        i = struct.unpack("<i", line)[0]
        return i
    elif mode == "float":
        f = struct.unpack("<f", line)[0]
        f = round(f, 4)
        return f
    elif mode == "char":
        c = struct.unpack("<b", int(line).to_bytes(1, "little"))[0]
        return c
    elif mode == "uchar":
        c = struct.unpack("<B", int(line).to_bytes(1, "little"))[0]
        return c
    else:
        return None

f = open("rail304.csv")
lines = f.readlines()
f.close()

lines.pop(0)

railInfoList = []
for line in lines:
    line = line.strip()
    arr = line.split(",")

    rail_data = int(arr[14])
    railInfo = []
    for i in range(rail_data):
        for j in range(i*8):
            railInfo.append(int(arr[15+j]))

    railInfoList.append(railInfo)

f = open("RAIL304.BIN", "rb")
line = f.read()
f.close()
byteArr = bytearray(line)

index = 0x1496
print("Read Map Data...")

mapCnt = readBinary(line[index:index+2], "short")
index += 2

for i in range(mapCnt):
    prev_rail = readBinary(line[index:index+2], "short")
    index += 2
    block = readBinary(line[index], "char")
    index += 1

    #vector
    for j in range(3):
        f = readBinary(line[index:index+4], "float")
        index += 4

    mdl_no = readBinary(line[index], "char")
    index += 1

    mdl_flg = readBinary(line[index], "char")
    index += 1

    mdl_kasenchu = readBinary(line[index], "char")
    index += 1

    per = readBinary(line[index:index+4], "float")
    index += 4
    
    #flg
    for j in range(4):
        index += 1

    #rail_data
    rail_data = line[index]
    index += 1

    railInfo = railInfoList[i]
    for rail in railInfo:
        bRail = struct.pack("<h", rail)
        for n in bRail:
            byteArr[index] = n
            index += 1

print("Map End!")

w = open("RAIL304.BIN", "wb")
w.write(byteArr)
w.close()
