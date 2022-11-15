import os
import re


def file_rename(pos, target_str, replace_str):
    r = re.search('(.*)_(.*)_(.*)_(.*)_(.*)_(.*)', target_str)
    file_name = {0: r.group(0), 1: r.group(1), 2: r.group(2), 3: r.group(3), 4: r.group(4), 5: r.group(5),
                 6: r.group(6)}

    for p in range(len(pos)):
        file_name[pos[p]] = replace_str[p]

    o_str = f'{file_name[1]}_{file_name[2]}_{file_name[3]}_{file_name[4]}_{file_name[5]}_{file_name[6]}'
    return o_str


def file_entity_rename(srcFile, dstFile):
    try:
        os.rename(srcFile, dstFile)
    except Exception as e:
        print(e)
        print('rename file fail\r\n')
    else:
        print('rename file success\r\n')


def replace_char(s, idx, ch):
    import ctypes
    OFFSET = ctypes.sizeof(ctypes.c_size_t) * 5
    a = ctypes.c_char.from_address(id(s) + OFFSET)
    pi = ctypes.pointer(a)
    pi[idx] = ch

# if __name__ == "__main__":
#     str = 'X-origin-213124124-X-VX-gank.wav'
#     pos = [2, 3, 5]
#     a = file_rename(pos, str, ['test', '3214123', 'VD'])
#     print(a)
