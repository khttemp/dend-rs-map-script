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
reverseFlag = True

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
    if reverseFlag:
        rsHeader = b'DEND_MAP_VER0400'
    else:
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

    endcntList = []
    #Map   
    print("Read Map Data...")

    mapCnt = readBinary(line[index:index+2], "short")
    newLine.extend(line[index:index+2])
    index += 2

    railInfoList = []
    reverseInfoList = []
    railDict = {}
    railLenDict = {}
    for i in range(mapCnt):
        railInfo = []
        reverseInfo = []
        readFlag = False
        prev_rail = readBinary(line[index:index+2], "short")
        railInfo.append(line[index:index+2])
        index += 2
        if prev_rail == -1:
            readFlag = True

        block = readBinary(line[index], "char")
        railInfo.append([line[index]])
        index += 1

        #vector
        xyz = []
        for j in range(3):
            railInfo.append(line[index:index+4])
            index += 4

        mdl_no = readBinary(line[index], "char")
        railInfo.append([line[index]])
        index += 1

        mdl_flg = readBinary(line[index], "char")
        railInfo.append([line[index]])
        index += 1

        mdl_kasenchu = readBinary(line[index], "char")
        railInfo.append([line[index]])
        index += 1

        per = readBinary(line[index:index+4], "float")
        railInfo.append(line[index:index+4])
        index += 4

        #flg
        for j in range(4):
            railInfo.append([line[index]])
            index += 1

        #rail_data
        rail_data = line[index]
        railInfo.append([line[index]])
        index += 1
        
        railDict[i] = int(rail_data)

        tempInfo = []
        for j in range(rail_data):
            next_rail = readBinary(line[index:index+2], "short")
            railInfo.append(line[index:index+2])
            index += 2
            
            next_no = readBinary(line[index:index+2], "short")
            railInfo.append(line[index:index+2])
            index += 2
            
            prev_rail = readBinary(line[index:index+2], "short")
            railInfo.append(line[index:index+2])
            index += 2
            
            prev_no = readBinary(line[index:index+2], "short")
            railInfo.append(line[index:index+2])
            index += 2

            if prev_rail not in railLenDict:
                railLenDict[prev_rail] = prev_no % 100
            else:
                if railLenDict[prev_rail] != prev_no % 100:
                    print("{0} Rail Length error!{1},{2}".format(prev_rail, railLenDict[prev_rail], prev_no % 10))

            if reverseFlag:
                tempInfo.extend([next_rail, next_no, prev_rail, prev_no])

        for j in range(len(tempInfo)):
            if j % 2 == 0:
                if j % 4 == 0:
                    temp2 = [tempInfo[j], 7]
                elif j % 4 == 2:
                    temp2 = [tempInfo[j], 0]
                    
                temp2.extend(reverseInfo)
                reverseInfo = temp2

        if len(reverseInfo) > 4:
            reverseInfo[5] = 100
            reverseInfo[7] = 107

        endcnt = line[index]
        index += 1
        if endcnt > 0:
            eList = []
            eList.append(i)
            eList.append(endcnt)
            for j in range(endcnt):
                for k in range(8):
                    eList.append(line[index+k])
                index += 0x08
            endcntList.append(eList)
        if readFlag:
            index += 0x1A

        railInfoList.append(railInfo)
        reverseInfoList.append(reverseInfo)

    if reverseFlag:
        for i in range(len(railInfoList)):
            railInfo = railInfoList[i]
            reverseInfo = reverseInfoList[i]
            for j in range(len(reverseInfo)):
                if j % 2 == 0:
                    railNo = reverseInfo[j]
                    if railNo == -1:
                        reverseInfo[j+1] = -1
                    else:
                        # 単線レール対応
                        if railDict[railNo] == 1 and reverseInfo[j+1] >= 100:
                            reverseInfo[j+1] = reverseInfo[j+1] % 100
                        # 長さ対応
                        if railNo in railLenDict and railLenDict[railNo] != 7 and reverseInfo[j+1] % 10 == 7:
                            reverseInfo[j+1] = reverseInfo[j+1] - 7 + railLenDict[railNo]

            for reverse in reverseInfo:
                rail = struct.pack("<h", reverse)
                railInfo.append(rail)
        
    for railInfo in railInfoList:
        for rail in railInfo:
            newLine.extend(rail)

    print("Map End!")

    cnt = struct.pack("<h", len(endcntList))
    for n in cnt:
        newLine.append(n)

    for i in range(len(endcntList)):
        railNo = endcntList[i][0]
        no = struct.pack("<h", railNo)
        for n in no:
            newLine.append(n)

        endcnt = endcntList[i][1]
        newLine.append(endcnt)

        for j in range(endcnt):
            for k in range(8):
                newLine.append(endcntList[i][8*j + k + 2])

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
