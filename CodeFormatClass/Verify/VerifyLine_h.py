# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/10/21
# 文件名       ：VerifyLine_h
# 文件简介     ：
# 文件说明     ：

"""
    本文件中所有的处理都是检测
"""
import re

from CodeFormatClass.InfoMsg.InfoMsg import *


# 这个处理头文件包含顺序问题
def VerifyIncludes(filename, lines):
    lint = []

    # 【\s*】 是用来处理类似这种情况的  【#    include <stdio.h>】
    include_config_re = re.compile(r'^#\s*include "(.*)"')
    include_system_re = re.compile(r'^#\s*include <(.*)>')

    STDAFX_HEADERS = 'stdafx.h'

    line_num = 1
    prev_config_header = None
    prev_system_header = None
    for line in lines:

        # Process Config/* headers
        config_header = include_config_re.match(line)
        if config_header:
            curr_config_header = config_header.group(1)

            # 判断当前头文件是不是 stdafx.h
            # 判断是 stdafx
            if curr_config_header.lower() == STDAFX_HEADERS.lower():
                # 如果是，那么就必须在最前面
                if prev_config_header or prev_system_header:
                    lint.append(InfoMsg(filename, line_num, '预编译头文引用必须位于所有头文件的第一个: #include "' + curr_config_header + '"'))
            # 不是 stdafx
            else:
                if prev_config_header:
                    if prev_config_header > curr_config_header:
                        lint.append(InfoMsg(filename, line_num, '头文件顺序异常，当前: "' + prev_config_header + '" 在 "' + curr_config_header + '" 前面'))

                # 只有在不是的时候，才往后传
                prev_config_header = curr_config_header

        # Process system headers
        system_header = include_system_re.match(line)
        if system_header:
            curr_system_header = system_header.group(1)

            if curr_system_header.lower() == STDAFX_HEADERS.lower():
                if prev_config_header or prev_system_header:
                    lint.append(InfoMsg(filename, line_num, '预编译头文引用必须位于所有头文件的第一个: #include <' + curr_system_header + '>'))
            else:
                if prev_system_header:
                    # Make sure system headers are alphabetized amongst themselves
                    if prev_system_header > curr_system_header:
                        lint.append(InfoMsg(filename, line_num, '头文件顺序异常，当前: <' + prev_system_header + '> 在 <' + curr_system_header + '> 前面'))

                prev_system_header = curr_system_header

        line_num += 1

    return lint


# 这个处理 Tab 还是空格缩进的问题
def VerifyTabs(filename, lines):
    lint = []
    tab_re = re.compile(r'\t')
    line_num = 1
    for line in lines:
        if tab_re.match(line.rstrip('\n')):
            lint.append(InfoMsg(filename, line_num, '发现了一个 TAB'))
        line_num += 1
    return lint


# 这个处理空格缩进的问题
def VerifySpace(filename, lines):
    lint = []
    tab_re = re.compile(r'^\s+')
    line_num = 1
    for index in range(len(lines)):
        line = lines[index]
        strSub = tab_re.match(line.rstrip('\n'))
        if strSub:
            for it in strSub.group(0):
                if it == ' ':
                    lint.append(InfoMsg(filename, line_num, '发现了空格开头'))
                    break
        line_num += 1
    return lint, lines


# 处理尾随空格的问题
def VerifyTrailingWhitespace(filename, lines):
    lint = []
    trailing_whitespace_re = re.compile(r'.*\s+$')
    line_num = 1
    for line in lines:
        line_rule = trailing_whitespace_re.match(line.rstrip('\n'))
        if line_rule:
            lint.append(InfoMsg(filename, line_num, '发现尾随空格，能删了就删了'))
        line_num += 1
    return lint


# 处理连续两个换行
def VerifyDoubleBlankLine(filename, lines):
    lint = []
    line_num = 1
    for index in range(len(lines)):
        line = lines[index]
        # 如果当前行是空行
        if line.rstrip('\n') == "":
            if index > 0:
                # 如果上一行也是空行
                strlast = lines[index - 1].rstrip('\n')
                if strlast == "":
                    lint.append(InfoMsg(filename, line_num, '发现了连续多行空行'))
        line_num += 1
    return lint


# 处理大括号后，第一个就是换行
def VerifyBlankLine(filename, lines):
    lint = []
    line_num = 1
    for index in range(len(lines)):
        line = lines[index]
        # 如果当前行是空行
        if line.rstrip('\n') == "":
            if index > 0:
                # 如果上一行是 {
                strlast = lines[index - 1].rstrip('\n')
                if strlast.endswith('{'):
                    lint.append(InfoMsg(filename, line_num, '发现了多余空行'))
        line_num += 1
    return lint


# 检测这一行是否只有空白字符
def VerifySpaceLine(filename, lines):
    lint = []
    trailing_whitespace_re = re.compile(r'^\s+$')
    line_num = 1
    for line in lines:
        line_rule = trailing_whitespace_re.match(line.rstrip('\n'))
        if line_rule:
            lint.append(InfoMsg(filename, line_num, '发现空白行'))
        line_num += 1
    return lint


# 处理 == 两侧，将右值放左边
def VerifyLogicEqual(filename, lines):
    flags = [".*==.*", ".*!=.*"]
    values = ["NULL", "TRUE", "FALSE", "true", "false", "nullptr"]
    lint = []
    line_num = 1

    # 循环判断两个比较
    for flag in flags:
        # 循环判断每一行代码
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
                        lint.append(InfoMsg(filename, line_num, '找到了一行 == 异常：' + line))
            line_num += 1

    return lint, lines
