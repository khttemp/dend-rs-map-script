#include <iostream>
#include <fstream>
#include <cstring>
#include <string>
#include <sstream>
#include <iomanip>
#include <Windows.h>
using namespace std;

short readShort(char* str) {
    char* buf = new char[2];
    memcpy(buf, str, 2);
    short *p = (short *)buf;
    return *p;
}

int readInt(char* str) {
    char* buf = new char[4];
    memcpy(buf, str, 4);
    int *p = (int *)buf;
    return *p;
}

float readFloat(char* str) {
    char* buf = new char[4];
    memcpy(buf, str, 4);
    float *p = (float *)buf;
    return *p;
}

string readString(char* str, int length) {
    char* buf = new char[length];
    memcpy(buf, str, length);
    buf[length] = '\0';

    return string(buf, length);
}

int main() {
    SetConsoleOutputCP(CP_UTF8);

    string sbuf;
    string input;
    cout << "DEND MAP SCRIPT ver1.0.0..." << endl;
    cout << "railのbinファイル名を入力してください: ";
    cin >> input;

    ifstream fin(input, ios::in | ios::binary);
    if (!fin) {
        cin.ignore();
        cout << "指定されたファイルが見つかりません。終了します。" << endl;
        getchar();
        return -1;
    }

    printf("見つけました！\n\n");
    fin.seekg(0, ios::end);
    int size = fin.tellg();
    fin.seekg(0, ios::beg);
    char* str = new char[size];
    fin.read(str, size);

    fin.close();

    int index = 16;
    bool readFlag = false;
    sbuf = readString(&str[0], index);

    if (sbuf != "DEND_MAP_VER0300" && sbuf != "DEND_MAP_VER0400") {
        cin.ignore();
        cout << "DEND map scriptファイルではありません。終了します。" << endl;
        cout << sbuf << endl;
        getchar();
        return -1;
    }

    if (sbuf == "DEND_MAP_VER0400") {
        readFlag = true;
    }

    int musicCnt = str[index];
    index++;
    for (int i = 0; i < musicCnt; i++) {
        index++;
    }

    int pRailCnt = str[index];
    index++;
    for (int i = 0; i < pRailCnt; i++) {
        for (int k = 0; k < 4; k++) {
            index += 2;
        }
        printf("\n");
        index++;
    }

    // unknown(1)
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 4; j++) {
            index += 2;
        }
        index++;
    }
    // unknown(1)
    
    index++;
    // 描画量? (1700)
    index += 4;
    
    //unknown(2)
    int unknownCnt = str[index];
    index++;
    for (int i = 0; i < unknownCnt; i++) {
        for (int j = 0; j < 2; j++) {
            index += 4;
        }
        index += 3;
    }
    //unknown(2)

    cout << "Read Light..." << endl;
    int lightCnt = str[index];
    index++;
    for (int i = 0; i < lightCnt; i++) {
        int b = str[index];
        index++;
        cout << i << " -> " << readString(&str[index], b) << endl;
        index += b;
    }
    cout << endl;

    cout << "Read png..." << endl;
    short pngCnt = readShort(&str[index]);
    index += 2;
    for (int i = 0; i < pngCnt; i++) {
        int b = str[index];
        index++;
        cout << i << " -> " << readString(&str[index], b) << endl;
        index += b;
    }
    cout << endl;

    //unknown(3)
    short cnt = readShort(&str[index]);
    index += 2;
    for (int i = 0; i < cnt; i++) {
        index += 9;
    }
    //unknown(3)

    cout << "Read Object Bin..." << endl;
    int binCnt = str[index];
    index++;
    for (int i = 0; i < binCnt; i++) {
        int b = str[index];
        index++;
        cout << i << " -> " << readString(&str[index], b) << endl;
        index += b;
    }
    cout << endl;
    index += 4;

    index += 2;
    cout << "Read smf..." << endl;
    char* buf = new char[2];
    memcpy(buf, &str[index], 1);
    buf[1] = 0x00;
    delete buf;
    short* smfCnt = (short *)buf;
    index++;
    for (int i = 0; i < *smfCnt; i++) {
        int b = str[index];
        index++;
        cout << i << " -> " << readString(&str[index], b);
        index += b;

        cout << " [";
        for (int j = 0; j < 4; j++) {
            short num = readShort(&str[index]);
            cout << num << ", ";
            index += 2;
        }
        cout << "]" << endl;
    }
    cout << endl;

    cout << "Read Station Name..." << endl;

    int snameCnt = str[index];
    index++;

    SetConsoleOutputCP(932);
    for (int i = 0; i < snameCnt; i++) {
        int b = str[index];
        index++;
        cout << i << " -> [ ";
        if (b > 0) {
            string buf = readString(&str[index], b);
            index += b;

            cout << buf;
        }
        cout << " ] ";
        for (int j = 0; j < 3; j++) {
            cout << (int)str[index++] << ", ";
        }
        cout << endl;
        index += 26;
    }
    cout << endl;

    SetConsoleOutputCP(CP_UTF8);

    //unknown(4)
    if (str[index] == 0x01) {
        index += 0x12;
    } else {
        index++;
    }
    //unknown(4)

    cout << "Read cpu data..." << endl;
    int cpuCnt = str[index];
    index++;

    for (int i = 0; i < cpuCnt; i++) {
        cout << i << " -> ";
        //Rail.No
        short railNo = readShort(&str[index]);
        cout << railNo << ", ";
        index += 2;
        //CPU mode?
        cout << (int)str[index++] << ", ";
        cout << (int)str[index++] << ", ";
        //
        for (int j = 0; j < 4; j++) {
            float f = readFloat(&str[index]);
            cout << f << ", ";
            index += 4;
        }
        cout << endl;
    }
    cout << endl;

    cout << "Read comic bin data..." << endl;
    int comicbinCnt = str[index];
    index++;

    for (int i = 0; i < comicbinCnt; i++) {
        cout << i << " -> ";
        short comicName = readShort(&str[index]);
        cout << comicName << ", ";
        index += 2;
        cout << (int)str[index++] << ", ";
        cout << (int)str[index++] << ", ";
        cout << (int)str[index++] << ", " << endl;
    }
    cout << endl;

    cout << "Dosan data...?" << endl;
    int dosanCnt = str[index];
    index++;

    for (int i = 0; i < dosanCnt; i++) {
        cout << i << " -> ";
        cout << "s_rail : [";
        for (int j = 0; j < 3; j++) {
            short num = readShort(&str[index]);
            cout << num << ", ";
            index += 2;
        }
        cout << "], " << endl;

        cout << "    e_rail : [";
        for (int j = 0; j < 3; j++) {
            short num = readShort(&str[index]);
            cout << num << ", ";
            index += 2;
        }
        cout << "], " << endl;
        
        cout << "    offset : ";
        short num = readShort(&str[index]);
        cout << num << endl;
        index += 2;

        cout << "    ";
        for (int j = 0; j < 5; j++) {
            float f = readFloat(&str[index]);
            cout << f << ", ";
            index += 4;
        }

        num = readShort(&str[index]);
        cout << num << endl;
        index += 2;
    }
    cout << endl;

    cout << hex << index << dec << endl;
    cout << "Read Map Data..." << endl;
    bool flag;
    bool onlyDrift = true;
    short mapCnt = readShort(&str[index]);
    index += 2;
    for (int i = 0; i < mapCnt; i++) {
        flag = false;
        ostringstream oss;
        oss << "[";
        short rail_no = readShort(&str[index]);
        index += 2;
        oss << rail_no << ", ";
        char block = str[index];
        index++;
        oss << (int)block;
        oss << "]";

        oss << ", ";
        //vector
        oss << "[";
        for (int j = 0; j < 3; j++) {
            float xyz = readFloat(&str[index]);;
            index += 4;
            oss << xyz << ", ";
        }
        oss << "], ";
        oss << "[";
        short mdl_no = readShort(&str[index]);
        oss << mdl_no << ", ";
        index += 2;
        oss << (int)str[index] << "], ";
        index++;

        float per = readFloat(&str[index]);;
        oss << per << ", ";
        index += 4;

        int k = 0;
        char* flg = new char[4];
        memcpy(flg, &str[index], 4);
        index += 4;
        
        for (int j = 0; j < 4; j++) {
            oss << "0x";
            oss << hex << setfill('0') << setw(2) << (flg[k] & 0x000000FF) << dec << ", ";
            if (j == 3) {
                if ((flg[k] & 0x01) == 0x01) {
                    flag = true;
                }
                if ((flg[k] & 0x02) == 0x02) {
                    flag = true;
                }
                if ((flg[k] & 0x04) == 0x04) {
                    flag = true;
                }
            }
            k++;
        }
        delete flg;

        int rail_data = str[index];
        index++;

        for (int j = 0; j < rail_data; j++) {
            if (readFlag) {
                oss << "[";
                short next_rail = readShort(&str[index]);
                index += 2;
                oss << next_rail << ", ";
                short next_no = readShort(&str[index]);
                index += 2;
                oss << next_no << ", ";
                short prev_rail = readShort(&str[index]);
                index += 2;
                oss << prev_rail << ", ";
                short prev_no = readShort(&str[index]);
                index += 2;
                oss << prev_no << "], ";
            }
            oss << "[";
            short next_rail = readShort(&str[index]);
            index += 2;
            oss << next_rail << ", ";
            short next_no = readShort(&str[index]);
            index += 2;
            oss << next_no << ", ";
            short prev_rail = readShort(&str[index]);
            index += 2;
            oss << prev_rail << ", ";
            short prev_no = readShort(&str[index]);
            index += 2;
            oss << prev_no << "], ";
        }
        oss << endl;
        cout << oss.str();
        /*
        delete buf;
        if (!onlyDrift) {
            string str = oss.str();
            cout << str;
        } else {
            if (flag) {
                string str = oss.str();
                cout << str;
            }
        }
        */
    }

    /*
    cout << "正常に読み込みできました。終了します。" << endl;
    if (index < size) {
        cout << "注意！設定したコマンド数(" << count << ")は、書き込んだコマンド数より少なく設定されています" << endl;
    }
    getchar();
    */

    return 0;
}