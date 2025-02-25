# -*- coding: utf-8 -*-
# Copyright 2022 Hai Liang W.
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from markup.Module import Module
from markup.Transform import Transform


COMMENT_SYMBOL = "%%"
COMMENT_MIN_LEN = len(COMMENT_SYMBOL) * 2


class SkipObsidianComments(Module):
    """
    Module for skip Obsidian comment
    https://github.com/hailiang-wang/markup-markdown/issues/6
    """

    priority = 1.7

    def transform(self, data):
        transforms = []
        linenum = 0

        for line in data:
            stripped = line.strip()
            if len(stripped) < COMMENT_MIN_LEN:
                # keep %%, %%% and other short text
                pass
            elif stripped.startswith(COMMENT_SYMBOL) and stripped.endswith(COMMENT_SYMBOL):
                transform = Transform(linenum, "drop")
                transforms.append(transform)
            else:
                # others
                pass
            linenum = linenum + 1

        return transforms
