# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/10/21
# 文件名       ：CodeFormat.py
# 文件简介     ：
# 文件说明     ：

"""

"""

import sys
from CodeFormatClass.CodeFormatClass_h import *


def CppLintMain(filenames):
    cf = CodeFormatCF(True)
    msg = []

    for filename in filenames:
        info = cf.RunOnFile(filename)
        msg.extend(info)

    if len(msg) > 0:
        for info in msg:
            print('%s:%d:%s' % (info.file, info.line, info.msg))

    return 0


if __name__ == '__main__':
    sys.exit(CppLintMain(sys.argv[1:]))
