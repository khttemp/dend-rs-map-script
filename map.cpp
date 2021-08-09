#include <iostream>
#include <fstream>
#include <cstring>
#include <string>
#include <Windows.h>
#define CMD_MAX 574
using namespace std;

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

    /*
    int slowFlag;
    cout << "ReadComicDataを１行ずつ読みますか？(Y/N)";
    while (true) {
        cin >> input;

        if (input == "Y" || input == "y") {
            slowFlag = 1;
            break;
        } else if (input == "N" || input == "n") {
            slowFlag = 0;
            break;
        } else {
            cin.ignore();
            cout << "入力エラー！改めて入力してください：";
        }
    }
    */

    int index = 16;
    char* buf = new char[index+1];
    memcpy(buf, &str[0], index);
    buf[index] = '\0';
    sbuf = string(buf);

    if (sbuf != "DEND_MAP_VER0300" && sbuf != "DEND_MAP_VER0400") {
        cin.ignore();
        cout << "DEND map scriptファイルではありません。終了します。" << endl;
        cout << sbuf << endl;
        getchar();
        return -1;
    }
    delete buf;

    int unknownCnt = str[index];
    index++;
    for (int i = 0; i < unknownCnt; i++) {
        index++;
    }

    unknownCnt = str[index];
    index++;
    for (int i = 0; i < 3; i++) {
        if (i == 1) {
            for (int j = 0; j < unknownCnt-1; j++) {
                index++;
                for (int k = 0; k < 4; k++) {
                    index += 2;
                }
            }
        } else {
            index++;
            for (int j = 0; j < 4; j++) {
                index += 2;
            }
            index++;
            for (int j = 0; j < 4; j++) {
                index += 2;
            }
        }
    }
    
    index++;
    /* 1700
    buf = new char[4];
    memcpy(buf, &str[index], 4);
    float* f = (float *)buf;
    cout << *f;
    cout << '\n';
    */

    index += 4;
    unknownCnt = str[index];
    index++;
    for (int i = 0; i < unknownCnt; i++) {
        for (int j = 0; j < 2; j++) {
            /*
            buf = new char[4];
            memcpy(buf, &str[index], 4);
            float* f = (float *)buf;
            cout << *f << ", ";
            */
            index += 4;
        }
        index += 3;
    }

    cout << "Read Light..." << endl;
    int lightCnt = str[index];
    index++;
    for (int i = 0; i < lightCnt; i++) {
        int b = str[index];
        index++;
        char* buf = new char[b+1];
        memcpy(buf, &str[index], b);
        buf[b] = '\0';
        cout << i << " -> " << buf << endl;
        index += b;
        delete buf;
    }
    cout << endl;

    cout << "Read png..." << endl;
    buf = new char[2];
    memcpy(buf, &str[index], 2);
    index += 2;
    short* cnt = (short *)buf;
    for (int i = 0; i < *cnt; i++) {
        int b = str[index];
        index++;
        char* buf = new char[b+1];
        memcpy(buf, &str[index], b);
        buf[b] = '\0';
        cout << i << " -> " << buf << endl;
        index += b;
        delete buf;
    }
    delete buf;
    cout << endl;

    buf = new char[2];
    memcpy(buf, &str[index], 2);
    index += 2;
    cnt = (short *)buf;
    for (int i = 0; i < *cnt; i++) {
        index += 9;
    }
    delete buf;

    cout << "Read Object Bin..." << endl;
    int binCnt = str[index];
    index++;
    for (int i = 0; i < binCnt; i++) {
        int b = str[index];
        index++;
        char* buf = new char[b+1];
        memcpy(buf, &str[index], b);
        buf[b] = '\0';
        cout << i << " -> " << buf << endl;
        index += b;
        delete buf;
    }
    cout << endl;
    index += 4;

    index += 2;
    cout << "Read smf..." << endl;
    buf = new char[2];
    memcpy(buf, &str[index], 1);
    buf[1] = 0x00;
    short* smfCnt = (short *)buf;
    index++;
    for (int i = 0; i < *smfCnt; i++) {
        int b = str[index];
        index++;
        char* buf = new char[b+1];
        memcpy(buf, &str[index], b);
        buf[b] = '\0';
        cout << i << " -> " << buf;
        index += b;
        delete buf;

        cout << " [";
        buf = new char[8];
        memcpy(buf, &str[index], 8);
        for (int j = 0; j < 4; j++) {
            short* num = (short *)&buf[j*2];
            cout << *num << ", ";
            index += 2;
        }
        cout << "]" << endl;
        delete buf;
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
            char* buf = new char[b+1];
            memcpy(buf, &str[index], b);
            buf[b] = '\0';
            index += b;

            cout << buf;
            delete buf;
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

    //unknown parameter
    if (str[index] == 0x01) {
        index += 0x12;
    } else {
        index++;
    }
    //unknown

    cout << "Read cpu data..." << endl;
    int cpuCnt = str[index];
    index++;

    for (int i = 0; i < cpuCnt; i++) {
        cout << i << " -> ";
        char* buf = new char[2];
        memcpy(buf, &str[index], 2);
        //Rail.No
        short* railNo = (short *)buf;
        cout << *railNo << ", ";
        index += 2;
        delete buf;
        //CPU mode?
        cout << (int)str[index++] << ", ";
        cout << (int)str[index++] << ", ";
        //
        buf = new char[16];
        memcpy(buf, &str[index], 16);
        for (int j = 0; j < 4; j++) {
            float* f = (float *)&buf[j*4];
            cout << *f << ", ";
        }
        index += 16;
        delete buf;
        cout << endl;
    }
    cout << endl;

    cout << "Read comic bin data..." << endl;
    int comicbinCnt = str[index];
    index++;

    for (int i = 0; i < comicbinCnt; i++) {
        cout << i << " -> ";
        char* buf = new char[2];
        memcpy(buf, &str[index], 2);

        short* comicName = (short *)buf;
        cout << *comicName << ", ";
        index += 2;
        cout << (int)str[index++] << ", ";
        cout << (int)str[index++] << ", ";
        cout << (int)str[index++] << ", " << endl;
        delete buf;
    }
    cout << endl;
    
    /*

    cout << "ReadComicData..." << endl;
    index++;

    buf = new char[2];
    memcpy(buf, &str[index], 2);
    short* p_num = (short *)buf;
    short num = *p_num;
    index += 2;
    delete buf;

    int count = 0;
    cin.ignore();
    for (int i = 0; i < num; i++) {
        if (index >= size) {
            cout << "注意！設定したコマンド数(" << num << ")は、書き込んだコマンド数(" << count << ")より多く読もうとしています" << endl;
            getchar();
            return 0;
        }
        cout << "No." << dec << i << " -> index(";
        cout << hex << index;
        cout << ")" << endl;
        char* buf = new char[2];
        memcpy(buf, &str[index], 2);
        short *p_num2 = (short *)buf;
        short num2 = *p_num2;
        index += 2;

        if (num2 < 0 || num2 >= CMD_MAX) {
            cout << "定義されてないコマンド番号です(" << dec << num2 << ")。読込を終了します。" << endl;
            getchar();
            return 0;
        }
        delete buf;
        
        cout << "cmd -> " << cmd[num2] << "(";
        cout << dec << num2 << ")" << endl;
        int b = str[index];
        index++;
        if (b >= 16) {
            cout << "script Error!" << endl;
            b = 16;
        }
        cout << "cmd_cnt -> " << b << endl;
        cout << "cmd_param -> [";
        for (int j = 0; j < b; j++) {
            float* f = (float *)&str[index];
            cout << *f << ", ";
            index += 4;
        }
        cout << "]" << endl;
        cout << '\n';
        count++;
    }

    cout << "正常に読み込みできました。終了します。" << endl;
    if (index < size) {
        cout << "注意！設定したコマンド数(" << count << ")は、書き込んだコマンド数より少なく設定されています" << endl;
    }
    getchar();
    */

    return 0;
}