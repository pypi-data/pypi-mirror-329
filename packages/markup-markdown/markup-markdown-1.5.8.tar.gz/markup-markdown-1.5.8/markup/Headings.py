#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ===============================================================================
#
# Copyright (c) 2020 <> All Rights Reserved
#
#
# File: /c/Users/Administrator/git/markup-markdown/markup/headings
# Author: Hai Liang Wang
# Date: 2023-03-09:06:41:55
#
# ===============================================================================

"""
   
"""
__copyright__ = "Copyright (c) 2020 . All Rights Reserved"
__author__ = "Hai Liang Wang"
__date__ = "2023-03-09:06:41:55"

import os
import sys
curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curdir)

if sys.version_info[0] < 3:
    raise RuntimeError("Must be using Python 3")
else:
    unicode = str


# Get ENV
ENVIRON = os.environ.copy()
CODEBLOCK_PREFIX = "```"

##########################################################################
# Testcases
##########################################################################
import unittest

# run testcase: python /c/Users/Administrator/git/markup-markdown/markup/headings Test.testExample


class Test(unittest.TestCase):
    '''

    '''

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        print("test_001")


def test():
    suite = unittest.TestSuite()
    suite.addTest(Test("test_001"))
    runner = unittest.TextTestRunner()
    runner.run(suite)


def main():
    test()


def is_codeblock_start(line: str, afters):
    '''
    Check if a code block
    '''
    # print("[is_codeblock_start] line", line)
    if line.startswith(CODEBLOCK_PREFIX):
        removed = line.replace(CODEBLOCK_PREFIX, "", 1)
        if len(removed.split(" ")) > 1:
            return False

        is_pair = False
        for x in afters:
            if x.strip() == CODEBLOCK_PREFIX:
                is_pair = True
                break

        if is_pair:
            return True
    else:
        return False


def parse_heading(line):
    if line.startswith("#"):
        level = []
        for x in range(len(line)):
            if line[x] == "#" and len(line) > (len(level) + 1) and line[len(level) + 1] in [" ", "#"]:
                level.append(x)
            else:
                break

        title = None

        if len(level) == 0:
            return False, None

        title = line[len(level) + 1:].strip()

        if not title:
            return False, None
        else:
            return len(level), title

    else:
        return False, None


def modify(line, append, lvl, title):

    new_lvl = lvl + append

    if new_lvl <= 0:
        raise RuntimeError("Invalid append value %d for line: %s \n [ERROR] new level must >= 1, which is %s in this case" % (append, line, new_lvl))

    return "#" * new_lvl + " " + title + "\n"


def shift_headings(append, input_lines):
    '''
    Shift headings
    '''
    # print("[shift_headings] append %s" % append)
    output_lines = []
    total_len = len(input_lines)

    is_codeblock = False

    for x in range(total_len):
        ll = input_lines[x]
        if is_codeblock:
            if ll.startswith(CODEBLOCK_PREFIX):
                is_codeblock = False
        elif not is_codeblock and is_codeblock_start(ll, input_lines[x + 1:]):
            is_codeblock = True
        else:
            # not code block, process headings
            lvl, title = parse_heading(ll)
            if lvl > 0:
                output_lines.append(modify(ll, append, lvl, title))
                continue

        output_lines.append(ll)

    return output_lines


def up(args):
    '''
    Level up headings
    '''
    INPUT_LINES = []
    with open(args.input, "r", encoding="utf-8") as fin:
        INPUT_LINES = [x for x in fin.readlines()]

    output = shift_headings(-args.append, INPUT_LINES)

    with open(args.output, "w") as fout:
        fout.writelines(output)

    return 0


def down(args):
    '''
    Level down headings
    '''
    INPUT_LINES = []
    with open(args.input, "r", encoding="utf-8") as fin:
        INPUT_LINES = [x for x in fin.readlines()]

    output = shift_headings(args.append, INPUT_LINES)

    with open(args.output, "w") as fout:
        fout.writelines(output)

    return 0


if __name__ == '__main__':
    main()
