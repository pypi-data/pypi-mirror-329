# -*- coding: utf-8 -*-
# Copyright 2023 Hai Liang W.
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from markup.Module import Module
from markup.Transform import Transform
import markup.Markers as Markers


class SkipHeaderMetadata(Module):
    """
    Module for skip header metadata, lines between -
    Headers Metadata Block
    ---
    xxx
    xxx
    ---
    """

    priority = 0.1

    def transform(self, data):
        transforms = []
        linenum = 0

        line_1st = data[0] if len(data) > 0 else None

        if line_1st is None:
            '''
            File without except or excerpt
            '''
            return None

        line_1st = line_1st.strip()

        if line_1st != Markers.markup_markdown_excerpt_begin:
            return None

        is_1st = True
        skipped = True
        for line in data:
            if is_1st:
                is_1st = False
                transform = Transform(linenum=linenum, oper="drop")
                transforms.append(transform)
                linenum = linenum + 1
                continue

            stripped = line.strip()

            if skipped is True and stripped == Markers.markup_markdown_excerpt_end:
                skipped = False
                transform = Transform(linenum, "drop")
                transforms.append(transform)
            elif skipped is False:
                transform = Transform(linenum, "noop")
                transforms.append(transform)
            else:
                # skipped is True and not equal to ---
                transform = Transform(linenum, "drop")
                transforms.append(transform)

            linenum = linenum + 1

        return transforms
