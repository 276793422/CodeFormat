# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/10/22
# 文件名       ：RepairLine_h.py
# 文件简介     ：
# 文件说明     ：

"""
    这里的所有处理，都是指修复，
    这里所有的函数，都返回两个值，第一个值是修改的内容，第二个值是新的文件行数组
"""
import math
import re

from CodeFormatClass.InfoMsg.InfoMsg import *


# 这个处理头文件包含顺序问题
def RepairIncludes(filename, lines):
    lint = []

    include_config_re = re.compile(r'^#include "(.*)"')
    include_system_re = re.compile(r'^#include <(.*)>')

    STDAFX_HEADERS = 'stdafx.h'
    STDAFX_STATUS = ['', '']

    prev_config_header = None
    prev_system_header = None

    # 第一个头文件所在的位置，还原插入的时候用
    head_first = 0
    # 头文件单独保存用的列表
    head_list = []
    # 循环用的数字
    line_num = 1
    for index in range(len(lines)):
        line = lines[index]
        # Process Config/* headers
        config_header = include_config_re.match(line)
        if config_header:

            # 第一个头文件的行号
            if head_first == 0:
                head_first = line_num

            curr_config_header = config_header.group(1)

            # 判断当前头文件是不是 stdafx.h
            # 判断是 stdafx
            if curr_config_header.lower() == STDAFX_HEADERS.lower():
                STDAFX_STATUS[0] = line
                # 如果是，那么就必须在最前面
                if prev_config_header or prev_system_header:
                    lint.append(
                        InfoMsg(filename, line_num, '预编译头文引用必须位于所有头文件的第一个: #include "' + curr_config_header + '"'))
            # 不是 stdafx
            else:
                # 记录当前头文件后面排序用
                head_list.append(line)

                if prev_config_header:
                    if prev_config_header > curr_config_header:
                        lint.append(InfoMsg(filename, line_num,
                                            '头文件顺序异常，已修复，之前: "' + prev_config_header + '" 在 "' + curr_config_header + '" 前面'))

                # 只有在不是的时候，才往后传
                prev_config_header = curr_config_header

        # Process system headers
        system_header = include_system_re.match(line)
        if system_header:

            if head_first == 0:
                head_first = line_num

            curr_system_header = system_header.group(1)

            if curr_system_header.lower() == STDAFX_HEADERS.lower():
                STDAFX_STATUS[1] = line
                if prev_config_header or prev_system_header:
                    lint.append(
                        InfoMsg(filename, line_num, '预编译头文引用必须位于所有头文件的第一个: #include <' + curr_system_header + '>'))
            else:
                head_list.append(line)

                if prev_system_header:
                    # Make sure system headers are alphabetized amongst themselves
                    if prev_system_header > curr_system_header:
                        lint.append(InfoMsg(filename, line_num,
                                            '头文件顺序异常，已修复，之前: <' + prev_system_header + '> 在 <' + curr_system_header + '> 前面'))

                prev_system_header = curr_system_header

        line_num += 1

    # 去重
    head_list = list(set(head_list))
    # 排序
    head_list.sort()

    # 把预编译头，放在最开始
    if STDAFX_STATUS[0] != '':
        head_list.insert(0, STDAFX_STATUS[0])
    elif STDAFX_STATUS[1] != '':
        head_list.insert(0, STDAFX_STATUS[1])

    # 补回去
    for index in range(len(head_list)):
        # 删除所有指定元素
        while head_list[index] in lines:
            lines.remove(head_list[index])
        lines.insert(head_first - 1, head_list[index])
        head_first += 1

    return lint, lines


# 这个处理 Tab 还是空格缩进的问题
def RepairTabs(filename, lines):
    lint = []
    tab_re = re.compile(r'\t')
    line_num = 1
    for index in range(len(lines)):
        line = lines[index]
        if tab_re.match(line.rstrip('\n')):
            lint.append(InfoMsg(filename, line_num, '发现了若干个 TAB ，每个 TAB 修复成 4 个 SPACE'))
            strNew = ""
            for i in range(len(line)):
                if line[i] == '\t':
                    strNew += "    "
                else:
                    strNew += line[i:len(line)]
                    break
            lines[index] = strNew
        line_num += 1
    return lint, lines


# 这个处理 Tab 还是空格缩进的问题
def RepairSpace(filename, lines):
    lint = []
    tab_re = re.compile(r'^\s+')
    line_num = 1
    bRemake = False
    for index in range(len(lines)):
        line = lines[index]
        strSub = tab_re.match(line.rstrip('\n'))
        if strSub:
            strSub = strSub.group(0)
            bRemake = False
            for it in strSub:
                if it == ' ':
                    lint.append(InfoMsg(filename, line_num, '发现了空格开头，每 4 个 空格，补成一个 TAB ，向上对齐'))
                    bRemake = True
                    break
            if bRemake is True:
                nspace = 0
                ntab = 0
                for it in strSub:
                    if it == ' ':
                        nspace += 1
                    elif it == '\t':
                        ntab += 1
                nCount = int(math.floor((nspace + 3) / 4))
                nCount += ntab
                lines[index] = (nCount * "\t") + line[len(strSub):]
        line_num += 1
    return lint, lines


# 处理尾随空格的问题
def RepairTrailingWhitespace(filename, lines):
    lint = []
    trailing_whitespace_re = re.compile(".*\s+$")
    line_num = 1
    for index in range(len(lines)):
        line = lines[index]
        line_rule = trailing_whitespace_re.match(line.rstrip('\n'))
        if line_rule:
            lint.append(InfoMsg(filename, line_num, '发现尾随空格，能删了就删了'))
            lines[index] = lines[index].rstrip()
        line_num += 1
    return lint, lines


# 处理连续两个换行
def RepairDoubleBlankLine(filename, lines):
    lint = []
    line_num = 1
    salt_num = 0
    for index in range(len(lines)):
        index -= salt_num
        # 这里重复判断，是因为lines 长度会改变，所以这里需要处理
        if index >= len(lines):
            break
        line = lines[index]
        # 如果当前行是空行
        if line.rstrip('\n') == "":
            if index > 0:
                # 如果上一行是 {
                strlast = lines[index - 1].rstrip('\n')
                if strlast == "":
                    lint.append(InfoMsg(filename, line_num, '发现了连续多行空行，已删除，只保留一行'))
                    # 删除指定的
                    del lines[index]
                    # 索引回退
                    salt_num += 1
                    # 行号回退
                    line_num -= 1
        line_num += 1
    return lint, lines


# 处理大括号后，第一个就是换行
def RepairBlankLine(filename, lines):
    lint = []
    line_num = 1
    salt_num = 0
    for index in range(len(lines)):
        index -= salt_num
        # 这里重复判断，是因为lines 长度会改变，所以这里需要处理
        if index >= len(lines):
            break
        line = lines[index]
        # 如果当前行是空行
        if line.rstrip('\n') == "":
            if index > 0:
                # 如果上一行是 {
                strlast = lines[index - 1].rstrip('\n')
                if strlast.endswith('{'):
                    lint.append(InfoMsg(filename, line_num, '发现了多余空行，已删除'))
                    # 删除指定的
                    del lines[index]
                    # 索引回退
                    salt_num += 1
                    # 行号回退
                    line_num -= 1
        line_num += 1
    return lint, lines


# 处理这一行如果只有空白字符，则处理为空行
def RepairSpaceLine(filename, lines):
    lint = []
    trailing_whitespace_re = re.compile(r'^\s+$')
    line_num = 1
    for index in range(len(lines)):
        line = lines[index]
        line_rule = trailing_whitespace_re.match(line.rstrip('\n'))
        if line_rule:
            lint.append(InfoMsg(filename, line_num, '发现空白行已经修复'))
            lines[index] = ""
        line_num += 1
    return lint, lines


# 处理 == 两侧，将右值放左边
def RepairLogicEqual(filename, lines):
    flags = [".*==.*", ".*!=.*"]
    values = ["NULL", "TRUE", "FALSE", "true", "false", "nullptr"]
    flaglist = ['=', '&&', '||', '!']
    lint = []

    # 循环判断两个比较
    for flag in flags:
        # 循环判断每一行代码
        line_num = 1
        for index in range(len(lines)):
            line = lines[index]
            # 判断一行代码
            if re.match(flag, line):
                # 找所有右值
                for value in values:
                    # 拼右值路径     ".*==.*NULL.*"
                    flag_str = ".*(" + flag + value + ".*).*"
                    flag_info = re.match(flag_str, line)
                    if flag_info:
                        str_out = "无法修复"
                        subflag = flag.replace(".*", "")
                        # 多个括号就不修复了，必须只有一个才修，符号也只能有一个，如果有多个的话，这里管不了
                        if line.count('(') == 1 and line.count(')') == 1 and line.count(subflag) == 1:
                            # 到这里就只剩下一个括号了，变成类似这样了  "(ZZZ == NULL)"
                            ileft = line.find('(')
                            iright = line.find(')')
                            # 前面已经判断了，左右都能找到，所以这里只需要判断顺序，避免出现  )(  这种
                            if ileft < iright:
                                # 得到   “ZZZ==NULL”
                                subline = line[ileft + 1: iright].replace(" ", "")
                                # 得到    ["ZZZ", "NULL"]
                                splitline = subline.split(subflag)
                                # 进来的规则就是只能有一个当前符号，所以这里必然有两个元素，不用判断了
                                ba = True
                                for chr in splitline[0]:
                                    if chr in flaglist:
                                        ba = False
                                        break
                                for chr in splitline[1]:
                                    if chr in flaglist:
                                        ba = False
                                        break

                                # 这个ba 的用途是判断是否是一个复合语句，比如如下：
                                #   (a == NULL || b != a)
                                #   (b != a || a == NULL)
                                if ba:
                                    # 交换，开头 + NULL + 空格 + == + 空格 + ZZZ + 结尾
                                    str = line[0: ileft + 1] + splitline[1] + " " + subflag + " " + splitline[0] + line[iright:]
                                    lines[index] = str
                                    str_out = "已经修复"
                        lint.append(InfoMsg(filename, line_num, '找到了一行 == 异常（' + str_out + '）：' + line))
            line_num += 1

    return lint, lines
