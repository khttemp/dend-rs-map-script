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
        return f
    else:
        return None

print("DEND MAP SCRIPT ver1.0.0...")
file = input("railのbinファイル名を入力してください: ")

readFlag = False

try:
    try:
        f = open(file, "rb")
        line = f.read()
        f.close()
    except FileNotFoundError:
        errorMsg = "指定されたファイルが見つかりません。終了します。"
        print(errorMsg)
        input()
        sys.exit()

    print("見つけました！")
    size = len(line)

    index = 16
    header = line[0:index]
    if header != b'DEND_MAP_VER0300' and header != b'DEND_MAP_VER0400':
        raise Exception

    if header == b'DEND_MAP_VER0400':
        readFlag = True

    #使う音楽(ダミーデータ?)
    musicCnt = line[index]
    index += 1
    for i in range(musicCnt):
        index += 1

    #配置する車両カウント
    trainCnt = line[index]
    print("初期配置カウント：{0}".format(trainCnt))
    index += 1
    print()

    print("初期位置")
    #3車両の初期レール位置
    for i in range(3):
        railNo = readBinary(line[index:index+2], "short")
        index += 2
        boneNo = readBinary(line[index:index+2], "short")
        index += 2

        ##########unknown
        index += 4
        index += 1
        ##########unknown
        print("{0} -> ({1}, {2})".format(i+1, railNo, boneNo))
    print()

    print("試運転位置")
    #試運転の初期レール位置
    railNo = readBinary(line[index:index+2], "short")
    index += 2
    boneNo = readBinary(line[index:index+2], "short")
    index += 2

    ##########unknown
    index += 4
    index += 1
    ##########unknown
    print("({0}, {1})".format(railNo, boneNo))
    print()

    #二人バトルの初期レール位置
    print("二人バトル位置")
    for i in range(2):
        railNo = readBinary(line[index:index+2], "short")
        index += 2
        boneNo = readBinary(line[index:index+2], "short")
        index += 2

        ##########unknown
        index += 4
        index += 1
        ##########unknown
        print("{0} -> ({1}, {2})".format(i+1, railNo, boneNo))
    print()

    index += 1

    ##########unknown
    print(readBinary(line[index:index+4], "float"))
    index += 4
    print()

    cnt = line[index]
    index += 1
    for i in range(cnt):
        for j in range(2):
            print(readBinary(line[index:index+4], "float"))
            index += 4
        index += 3
    print()
    ##########unknown
    
    #Light情報
    print("Read Light...")
    lightCnt = line[index]
    index += 1
    for i in range(lightCnt):
        b = line[index]
        index += 1
        text = line[index:index+b].decode()
        print("{0} -> {1}".format(i, text))
        index += b
    print()

    #png情報
    print("Read Png...")
    pngCnt = readBinary(line[index:index+2], "short")
    index += 2
    for i in range(pngCnt):
        b = line[index]
        index += 1
        text = line[index:index+b].decode()
        print("{0} -> {1}".format(i, text))
        index += b
    print()

    ##########unknown
    cnt = readBinary(line[index:index+2], "short")
    index += 2
    for i in range(cnt):
        index += 9
    ##########unknown

    print("Read Object Bin...")
    binCnt = line[index]
    index += 1
    for i in range(binCnt):
        b = line[index]
        index += 1
        text = line[index:index+b].decode()
        print("{0} -> {1}".format(i, text))
        index += b
    print()

    ##########unknown
    cnt = line[index]
    index += 1
    for i in range(cnt):
        index += 5
    ##########unknown
    
    print("Read smf...")
    smfCnt = line[index]
    index += 1
    for i in range(smfCnt):
        b = line[index]
        index += 1
        text = line[index:index+b].decode()
        index += b
        arr = []
        for j in range(4):
            n = readBinary(line[index:index+2], "short")
            arr.append(n)
            index += 2
        print("{0} -> {1}, {2}".format(i, text, arr))
    print()

    print("Read Station Name...")
    snameCnt = line[index]
    index += 1
    for i in range(snameCnt-1):
        b = line[index]
        index += 1
        text = ""
        if b > 0:
            text = line[index:index+b].decode("shift-jis")
            index += b
        arr = []
        for j in range(3):
            arr.append(line[index])
            index += 1
        index += 0x1A
        print("{0} -> {1}, {2}".format(i, text, arr))

    index += 1

    ##########unknown
    cnt = line[index]
    index += 1
    for i in range(cnt):
        index += 0x0E

    cnt = line[index]
    index += 1
    if cnt > 0:
        for i in range(cnt):
            index += 16

        index += 1
    print()
    ##########unknown
    
    #cpu
    print("Read cpu data...")
    cpuCnt = line[index]
    index += 1
    for i in range(cpuCnt):
        arr = []
        railNo = readBinary(line[index:index+2], "short")
        index += 2
        arr.append(railNo)
        
        org = line[index]
        index += 1
        arr.append(org)
        mode = line[index]
        index += 1
        arr.append(mode)

        for j in range(4):
            f = readBinary(line[index:index+4], "float")
            index += 4
            arr.append(f)
        print("{0} -> {1}".format(i, arr))
    print()

    #comic bin data
    print("Read comic bin data...")
    comicbinCnt = line[index]
    index += 1

    for i in range(comicbinCnt):
        arr = []
        comicName = readBinary(line[index:index+2], "short")
        index += 2
        arr.append(comicName)

        for j in range(3):
            arr.append(line[index])
            index += 1
        print("{0} -> {1}".format(i, arr))
    print()

    #Dosan data...?
    dosanCnt = line[index]
    index += 1

    for i in range(dosanCnt):
        print("{0} -> ".format(i))
        arr = []
        for j in range(3):
            num = readBinary(line[index:index+2], "short")
            index += 2
            arr.append(num)
        print("s_rail：{0}".format(arr))

        arr = []
        for j in range(3):
            num = readBinary(line[index:index+2], "short")
            index += 2
            arr.append(num)
        print("e_rail：{0}".format(arr))

        num = readBinary(line[index:index+2], "short")
        index += 2
        print("offset：{0}".format(num))

        arr = []
        for j in range(5):
            f = readBinary(line[index:index+4], "float")
            index += 4
            arr.append(f)
        print("float：{0}".format(arr))

        num = readBinary(line[index:index+2], "short")
        index += 2
        print("short：{0}".format(num))
    print()

    #Map
    print("Read Map Data...")
    mapCnt = readBinary(line[index:index+2], "short")
    index += 2

    for i in range(mapCnt):
        rail_no = readBinary(line[index:index+2], "short")
        index += 2
        block = line[index]
        index += 1

        print("{0} -> [{1},{2}], ".format(i, rail_no, block), end="")

        #vector?
        xyz = []
        for j in range(3):
            f = readBinary(line[index:index+4], "float")
            xyz.append(f)
            index += 4
        print("{0}, ".format(xyz), end="")

        mdl_no = line[index]
        index += 1

        mdl_no_next = readBinary(line[index:index+2], "short")
        index += 2

        per = readBinary(line[index:index+4], "float")
        index += 4

        print("[{0},{1}], {2}, ".format(mdl_no, mdl_no_next, per), end="")
        
        #flg
        flg = []
        for j in range(4):
            flg.append(hex(line[index]))
            index += 1
        print("{0}, ".format(flg), end="")

        #rail_data
        rail_data = line[index]
        index += 1

        for j in range(rail_data):
            if readFlag:
                next_rail = readBinary(line[index:index+2], "short")
                index += 2
                next_no = readBinary(line[index:index+2], "short")
                index += 2
                prev_rail = readBinary(line[index:index+2], "short")
                index += 2
                prev_no = readBinary(line[index:index+2], "short")
                index += 2

                print("[{0},{1},{2},{3}], ".format(next_rail, next_no, prev_rail, prev_no), end="")

            next_rail = readBinary(line[index:index+2], "short")
            index += 2
            next_no = readBinary(line[index:index+2], "short")
            index += 2
            prev_rail = readBinary(line[index:index+2], "short")
            index += 2
            prev_no = readBinary(line[index:index+2], "short")
            index += 2
            print("[{0},{1},{2},{3}], ".format(next_rail, next_no, prev_rail, prev_no), end="")

        print()
    input()
        
except Exception as e:
    print(e)
    sys.exit()


