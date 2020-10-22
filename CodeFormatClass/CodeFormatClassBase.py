# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/10/21
# 文件名       ：CodeFormatClass.py
# 文件简介     ：
# 文件说明     ：

"""

"""

from .CodeFormatClass_h import *


# 代码规范基类
class CodeFormatBase:

    def __init__(self, repair=False):
        self.repair = repair

    # 处理头文件
    def TestIncludes(self, filename, lines):
        lint = []
        # 先检测头文件包含
        if self.repair:
            lintTemp, lines = RepairIncludes(filename, lines)
        else:
            lintTemp = VerifyIncludes(filename, lines)

        return lintTemp, lines

    # 处理 Tab
    def TestTabs(self, filename, lines):
        lint = []
        # 检测是否是 TAB 缩进
        if self.repair:
            lintTemp, lines = RepairTabs(filename, lines)
        else:
            lintTemp = VerifyTabs(filename, lines)

        return lintTemp, lines

    def TestTrailingWhitespace(self, filename, lines):
        lint = []
        if self.repair:
            lintTemp, lines = RepairTrailingWhitespace(filename, lines)
        else:
            lintTemp = VerifyTrailingWhitespace(filename, lines)

        return lintTemp, lines


    def RunOnFile(self, filename):
        print("error CodeFormat Error \n")
        return []

