# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/10/21
# 文件名       ：Library.py
# 文件简介     ：
# 文件说明     ：

"""

"""


# 数据写入文件
def SaveStingArrayIntoFile(info, save_file, split=""):
    with open(save_file, "w") as f:
        for line in info:
            f.write(line + split)
    return save_file


# 加载一个文件到数组
def LoadFileToArray(path):
    file_line = []
    file = open(path, "r", errors='ignore')
    for line in file.readlines():
        line = line.strip('\n')
        file_line.append(line)
    file.close()
    return file_line
