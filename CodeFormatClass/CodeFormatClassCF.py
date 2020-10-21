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


# CF代码规范
class CodeFormatCF(CodeFormatBase):
    def RunOnFile(self, filename):
        lines = LoadFileToArray(filename)
        lint = []

        # 先检测头文件包含
        lint.extend(VerifyIncludes(filename, lines))

        lint.extend(VerifyTabs(filename, lines))

        lint.extend(VerifyTrailingWhitespace(filename, lines))

        return lint




