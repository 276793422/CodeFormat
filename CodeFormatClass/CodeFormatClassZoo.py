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


# 个人代码规范
class CodeFormatZoo(CodeFormatBase):

    def __init__(self, repair=False):
        self.repair = repair

    def RunOnFile(self, filename):
        lines = LoadFileToArray(filename)
        lint = []

        # 先检测头文件包含
        lintTemp, lines = self.TestIncludes(filename, lines)
        lint.extend(lintTemp)

        # 检测是否是 空格 缩进
        lintTemp, lines = self.TestSpace(filename, lines)
        lint.extend(lintTemp)

        # 检测行尾是否是空格
        lintTemp, lines = self.TestTrailingWhitespace(filename, lines)
        lint.extend(lintTemp)

        # 处理空白行
        lintTemp, lines = self.TestSpaceLine(filename, lines)
        lint.extend(lintTemp)

        # 删除大括号后面的空行
        lintTemp, lines = self.TestBlankLine(filename, lines)
        lint.extend(lintTemp)

        if len(lint) > 0:
            SaveStingArrayIntoFile(lines, filename, '\n')

        return lint


