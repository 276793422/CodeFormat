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


def CppLintMain():
    if len(sys.argv) == 1:
        return

    if len(sys.argv) == 2:
        return

    file_names = sys.argv[2:]
    format_type = sys.argv[1]

    cf = None
    if format_type == "cf":
        cf = CodeFormatCF(True)
        pass
    elif format_type == "zoo":
        cf = CodeFormatZoo(True)
        pass
    elif format_type == "custom":
        cf = CodeFormatCustom(True)
        pass
    else:
        cf = CodeFormatBase(True)

    if cf is None:
        return

    msg = []

    for filename in file_names:
        info = cf.RunOnFile(filename)
        msg.extend(info)

    if len(msg) > 0:
        for info in msg:
            print('%s:%d:%s' % (info.file, info.line, info.msg))
    else:
        print('代码合规，可以提交')

    return


if __name__ == '__main__':
    CppLintMain()
