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


print("DEND Convert CS to RS SCRIPT ver1.0.0...")
file = input("CSのrailのbinファイル名を入力してください: ")
fildDir = "."
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

    newLine = bytearray()
    rsHeader = b'DEND_MAP_VER0300'

    for n in rsHeader:
        newLine.append(n)

    startIdx = index
    
    #使う音楽(ダミーデータ?)
    musicCnt = line[index]
    index += 1
    for i in range(musicCnt):
        index += 1

    #配置する車両カウント
    trainCnt = line[index]
    index += 1

    #3車両の初期レール位置
    for i in range(trainCnt):
        railNo = readBinary(line[index:index+2], "short")
        index += 2
        boneNo = readBinary(line[index:index+2], "short")
        index += 2

        ########## rail pos unknown
        index += 4
        index += 1
        ########## rail pos unknown

    #ダミー位置？
    index += 2
    index += 2
    index += 4
    index += 1

    #試運転、二人バトルの初期レール位置
    for i in range(2):
        railNo = readBinary(line[index:index+2], "short")
        index += 2
        boneNo = readBinary(line[index:index+2], "short")
        index += 2

        ##########unknown
        index += 4
        index += 1
        ##########unknown

    index += 1
    ##########unknown
    index += 4

    cnt = line[index]
    index += 1
    for i in range(cnt):
        for j in range(2):
            index += 4
        index += 3
    ##########unknown
    
    #Light情報
    lightCnt = line[index]
    index += 1
    for i in range(lightCnt):
        b = line[index]
        index += 1
        index += b

    #png情報
    pngCnt = readBinary(line[index:index+2], "short")
    index += 2
    for i in range(pngCnt):
        b = line[index]
        index += 1
        text = line[index:index+b].decode()
        index += b

    ##########unknown
    cnt = readBinary(line[index:index+2], "short")
    index += 2
    for i in range(cnt):
        index += 9
    ##########unknown

    binCnt = line[index]
    index += 1
    for i in range(binCnt):
        b = line[index]
        index += 1
        text = line[index:index+b].decode()
        index += b

    ##########unknown
    cnt = line[index]
    index += 1
    for i in range(cnt):
        index += 5
    ##########unknown
    
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
        
    ##########unknown
    cnt = line[index]
    index += 1
    for i in range(cnt):
        index += 0x11
    ##########unknown
    
    #cpu
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

    #comic bin data
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

    #Dosan data
    dosanCnt = line[index]
    index += 1

    for i in range(dosanCnt):
        arr = []
        for j in range(3):
            num = readBinary(line[index:index+2], "short")
            index += 2
            arr.append(num)

        arr = []
        for j in range(3):
            num = readBinary(line[index:index+2], "short")
            index += 2
            arr.append(num)

        num = readBinary(line[index:index+2], "short")
        index += 2

        arr = []
        for j in range(5):
            f = readBinary(line[index:index+4], "float")
            index += 4
            arr.append(f)
        index += 2

    endIdx = index
    newLine.extend(line[startIdx:endIdx])

    #Map   
    print("Read Map Data...")

    mapCnt = readBinary(line[index:index+2], "short")
    newLine.extend(line[index:index+2])
    index += 2
    
    for i in range(mapCnt):
        readFlag = False
        prev_rail = readBinary(line[index:index+2], "short")
        newLine.extend(line[index:index+2])
        index += 2
        if prev_rail == -1:
            readFlag = True

        block = readBinary(line[index], "char")
        newLine.append(line[index])
        index += 1

        #vector
        xyz = []
        for j in range(3):
            newLine.extend(line[index:index+4])
            index += 4

        mdl_no = readBinary(line[index], "char")
        newLine.append(line[index])
        index += 1

        mdl_flg = readBinary(line[index], "char")
        newLine.append(line[index])
        index += 1

        mdl_kasenchu = readBinary(line[index], "char")
        newLine.append(line[index])
        index += 1

        per = readBinary(line[index:index+4], "float")
        newLine.extend(line[index:index+4])
        index += 4

        #flg
        for j in range(4):
            newLine.append(line[index])
            index += 1

        #rail_data
        rail_data = line[index]
        newLine.append(line[index])
        index += 1

        for j in range(rail_data):
            next_rail = readBinary(line[index:index+2], "short")
            newLine.extend(line[index:index+2])
            index += 2
            
            next_no = readBinary(line[index:index+2], "short")
            newLine.extend(line[index:index+2])
            index += 2
            
            prev_rail = readBinary(line[index:index+2], "short")
            newLine.extend(line[index:index+2])
            index += 2
            
            prev_no = readBinary(line[index:index+2], "short")
            newLine.extend(line[index:index+2])
            index += 2

        endcnt = line[index]
        index += 1
        for j in range(endcnt):
            print("{0}".format(i), end=", ")
            for k in range(8):
                print("{0}".format(line[index+k]), end=", ")
            print()
            index += 0x08
            
        if readFlag:
            index += 0x1A

    cnt = struct.pack("<h", 0)
    for n in cnt:
        newLine.append(n)

    for i in range(0):
        pass

    cnt = struct.pack("<h", 0)
    for n in cnt:
        newLine.append(n)

    newLine.extend(line[index:])

    w = open(filename.upper() + "_CONV.BIN", "wb")
    w.write(newLine)
    w.close()

except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    sys.exit()