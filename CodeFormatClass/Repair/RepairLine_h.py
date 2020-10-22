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

import re

from CodeFormatClass.InfoMsg.InfoMsg import *


# 这个处理头文件包含顺序问题
def RepairIncludes(filename, lines):
    lint = []

    include_config_re = re.compile(r'^#include "(.*)"')
    include_system_re = re.compile(r'^#include <(.*)>')

    STDAFX_HEADERS = 'stdafx.h'
    STDAFX_STATUS = ['','']

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
                    lint.append(InfoMsg(filename, line_num, '预编译头文引用必须位于所有头文件的第一个: #include "' + curr_config_header + '"'))
            # 不是 stdafx
            else:
                # 记录当前头文件后面排序用
                head_list.append(line)

                if prev_config_header:
                    if prev_config_header > curr_config_header:
                        lint.append(InfoMsg(filename, line_num, '头文件顺序异常，已修复，之前: "' + prev_config_header + '" 在 "' + curr_config_header + '" 前面'))

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
                    lint.append(InfoMsg(filename, line_num, '预编译头文引用必须位于所有头文件的第一个: #include <' + curr_system_header + '>'))
            else:
                head_list.append(line)

                if prev_system_header:
                    # Make sure system headers are alphabetized amongst themselves
                    if prev_system_header > curr_system_header:
                        lint.append(InfoMsg(filename, line_num, '头文件顺序异常，已修复，之前: <' + prev_system_header + '> 在 <' + curr_system_header + '> 前面'))

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
        pass

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


# 处理尾随空格的问题
def RepairTrailingWhitespace(filename, lines):
    lint = []
    trailing_whitespace_re = re.compile("\s+$")
    line_num = 1
    for line in lines:
        line_rule = trailing_whitespace_re.match(line.rstrip('\n'))
        if line_rule:
            lint.append(InfoMsg(filename, line_num, '发现尾随空格，能删了就删了'))
        line_num += 1
    return lint, lines


# 处理连续两个换行


# 处理大括号后，第一个就是换行





