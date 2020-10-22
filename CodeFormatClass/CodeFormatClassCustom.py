# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/10/23
# 文件名       ：CodeFormatClassCustom
# 文件简介     ：
# 文件说明     ：

"""

"""
from .CodeFormatClass_h import *


# 个人代码规范
class CodeFormatCustom(CodeFormatBase):

    def __init__(self, repair=False):
        self.repair = repair

    def RunOnFile(self, filename):
        lines = LoadFileToArray(filename)
        lint = []

        # 检测是否是 TAB 缩进
        lintTemp, lines = self.TestTabs(filename, lines)
        lint.extend(lintTemp)

        # 检测是否是 空格 缩进
        lintTemp, lines = self.TestSpace(filename, lines)
        lint.extend(lintTemp)

        if len(lint) > 0:
            SaveStingArrayIntoFile(lines, filename, '\n')

        return lint





