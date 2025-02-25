# -*- coding: utf-8 -*-
# Copyright 2022 Hai Liang W.
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


import os
from markup.Module import Module
from markup.Transform import Transform

VARIABLES = dict()
REPL_PREFIX_SYMBOL = "%"
VARIABLE_PREFIX = "MBN_"
LEN_VARIABLE_PREFIX = len(VARIABLE_PREFIX)


def is_zh(ch):
    """return True if ch is Chinese character.
    full-width puncts/latins are not counted in.
    """
    x = ord(ch)
    # CJK Radicals Supplement and Kangxi radicals
    if 0x2e80 <= x <= 0x2fef:
        return True
    # CJK Unified Ideographs Extension A
    elif 0x3400 <= x <= 0x4dbf:
        return True
    # CJK Unified Ideographs
    elif 0x4e00 <= x <= 0x9fbb:
        return True
    # CJK Compatibility Ideographs
    elif 0xf900 <= x <= 0xfad9:
        return True
    # CJK Unified Ideographs Extension B
    elif 0x20000 <= x <= 0x2a6df:
        return True
    else:
        return False


def read_envs():
    '''
    '''
    envs = os.environ.copy()
    for x in envs:
        if x.startswith("MBN_") and len(x) > LEN_VARIABLE_PREFIX:
            VARIABLES[x] = envs[x]


read_envs()


def repl(previous):
    '''
    Replacement
    '''
    aft = previous

    for k in VARIABLES.keys():
        v = VARIABLES[k]
        r = "%s%s%s" % (REPL_PREFIX_SYMBOL, k, REPL_PREFIX_SYMBOL)

        # print(previous, v[len(v) - 1], is_zh(v[len(v) - 1]))

        # consider the space formatter of chinese, reduce the space
        # if "%s " % r in aft and is_zh(v[len(v) - 1]):
        #     aft = aft.replace("%s " % r, v)

        aft = aft.replace(r, v)

    return aft


class EnvVariableReplacements(Module):
    """
    Module for skip Obsidian comment
    https://github.com/hailiang-wang/markup-markdown/issues/6
    """

    priority = 1.8

    def transform(self, data):
        transforms = []
        linenum = 0

        for line in data:
            stripped = line.strip()
            if line.startswith("%%") or line.startswith("<!--") or not stripped:
                # ignore comments
                pass
            else:
                updated = repl(line)
                transform = Transform(linenum, "swap", updated)
                transforms.append(transform)

            linenum = linenum + 1

        return transforms
