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

print("DEND MAP SCRIPT ver1.0.0...")
file = input("railのbinファイル名を入力してください: ")
fildDir = "../raildata/CS"
readFlag = False

try:
    try:
        filepath = os.path.join(fildDir, file)
        filename = os.path.splitext(file)[0]
        f = open(filepath, "rb")
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
    if header != b'DEND_MAP_VER0110':
        raise Exception

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

    #3車両の初期レール位置
    print("初期位置")
    for i in range(trainCnt):
        railNo = readBinary(line[index:index+2], "short")
        index += 2
        boneNo = readBinary(line[index:index+2], "short")
        index += 2

        ########## rail pos unknown
        index += 4
        index += 1
        ########## rail pos unknown
        print("{0} -> ({1}, {2})".format(i+1, railNo, boneNo))
    print()

    #ダミー位置？
    index += 2
    index += 2
    index += 4
    index += 1

    #試運転、二人バトルの初期レール位置
    print("試運転、二人バトル位置")
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
    for i in range(snameCnt):
        b = line[index]
        index += 1
        text = ""
        if b > 0:
            text = line[index:index+b].decode("shift-jis")
            index += b

        stFlag = line[index]
        index += 1
        railNo = readBinary(line[index:index+2], "short")
        index += 2
        index += 0x1A
        print("{0} -> {1}, {2}, {3}".format(i, text, stFlag, railNo))

    ##########unknown
    cnt = line[index]
    index += 1
    for i in range(cnt):
        index += 0x12
    print()
    ##########unknown

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

    #Dosan data
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

        index += 2
    print()

    
    #Map   
    print("Read Map Data...")
    w = open(filename + ".csv", "w")
    w.write("index,prev_rail,block,")
    w.write("dir_x,dir_y,dir_z,")
    w.write("mdl_no,mdl_flg,mdl_kasenchu,per,")
    w.write("flg,flg,flg,flg,")
    w.write("rail_data,")
    w.write("next_rail,next_no,prev_rail,prev_no,\n")
    mapCnt = readBinary(line[index:index+2], "short")
    index += 2

    for i in range(mapCnt):
        readFlag = False
        prev_rail = readBinary(line[index:index+2], "short")
        index += 2
        if prev_rail == -1:
            readFlag = True
        block = readBinary(line[index], "char")
        index += 1

        w.write("{0},{1},{2},".format(i, prev_rail, block))

        #vector
        xyz = []
        for j in range(3):
            f = readBinary(line[index:index+4], "float")
            xyz.append(f)
            index += 4
            w.write("{0},".format(f))

        mdl_no = readBinary(line[index], "char")
        index += 1
        w.write("{0},".format(mdl_no))

        mdl_flg = readBinary(line[index], "char")
        index += 1
        w.write("{0},".format(mdl_flg))

        mdl_kasenchu = readBinary(line[index], "char")
        index += 1
        w.write("{0},".format(mdl_kasenchu))

        per = readBinary(line[index:index+4], "float")
        index += 4
        w.write("{0},".format(per))
        
        #flg
        flg = []
        for j in range(4):
            flag = line[index]
            flg.append(flag)
            index += 1
            w.write("0x{:02x},".format(flag))

        #rail_data
        rail_data = line[index]
        w.write("{0},".format(rail_data))
        index += 1

        for j in range(rail_data):
            next_rail = readBinary(line[index:index+2], "short")
            index += 2
            next_no = readBinary(line[index:index+2], "short")
            index += 2
            prev_rail = readBinary(line[index:index+2], "short")
            index += 2
            prev_no = readBinary(line[index:index+2], "short")
            index += 2
            w.write("{0},{1},{2},{3},".format(next_rail, next_no, prev_rail, prev_no))

        endcnt = line[index]
        index += 1
        if endcnt > 0:
            print("{0}".format(i), end=", ")
            print("{0}".format(endcnt), end=", ")
            for j in range(endcnt):
                for k in range(8):
                    print("{0}".format(line[index+k]), end=", ")
                index += 0x08
            print()
        if readFlag:
            index += 0x1A

        w.write("\n")
    w.close()

    print("Map End!")

    print("amb data...")
    ambcnt = readBinary(line[index:index+2], "short")
    index += 2
    w = open(filename + "_amb.csv", "w")
    for i in range(ambcnt):
        temp = line[index]
        index += 1
        w.write("{0},".format(temp))
        temp = readBinary(line[index:index+4], "float")
        index += 4
        w.write("{0},".format(temp))
        for j in range(2):
            temp = readBinary(line[index:index+2], "short")
            index += 2
            w.write("{0},".format(temp))

        for j in range(6):
            temp = readBinary(line[index:index+4], "float")
            index += 4
            w.write("{0},".format(temp))

        temp = line[index]
        index += 1
        w.write("{0},".format(temp))
        temp = line[index]
        index += 1
        w.write("{0},".format(temp))

        temp = readBinary(line[index:index+2], "short")
        index += 2
        w.write("{0},".format(temp))

        for j in range(10):
            temp = readBinary(line[index:index+4], "float")
            index += 4
            w.write("{0},".format(temp))

        cnta = line[index]
        index += 1
        w.write("{0},".format(cnta))
        for j in range(cnta):
            temp = readBinary(line[index:index+2], "short")
            index += 2
            w.write("{0},".format(temp))

            for k in range(10):
                temp = readBinary(line[index:index+4], "float")
                index += 4
                w.write("{0},".format(temp))
        w.write("\n")
    w.close()

    print("amb End!")
except Exception as e:
    print(e)
    sys.exit()


