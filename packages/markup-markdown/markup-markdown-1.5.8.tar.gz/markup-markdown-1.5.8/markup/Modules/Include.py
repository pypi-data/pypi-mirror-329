# -*- coding: utf-8 -*-
# Copyright 2015 John Reese
# Modifications copyright (C) 2022 Hai Liang W.
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import glob
import os
import re
from os import path

from markup.Module import Module
from markup.Transform import Transform
import markup.Markers as Markers
from markup.Modules.SkipHeaderMetadata import SkipHeaderMetadata


skip_header_metadata = SkipHeaderMetadata()


def filter_by_block_heading_text(original, block_heading_text):
    """
    Filter out data by blocking heading text
    """
    ret = []

    total_len = len(original)
    heading_level = None
    heading_pos = None

    for x in range(total_len):
        ld = original[x].strip()
        ld_len = len(ld)
        if ld.startswith("#") and not ld.endswith("#"):
            heading_level = []
            for y in range(ld_len):
                if ld.startswith("#"):
                    heading_level.append("#")
                    ld = ld[1:]
                else:
                    break

            ld = ld.strip()
            if ld == block_heading_text:
                # pos and heading level found
                heading_pos = x
                break

    if heading_pos is not None:
        # print("[filter_by_block_heading_text] heading pos", heading_pos, ", heading level", len(heading_level))
        # get the data
        stop_symbol_data = []

        stop_symbol_prefix = ""
        for x in heading_level:
            stop_symbol_prefix = stop_symbol_prefix + "#"
            stop_symbol_data.append(stop_symbol_prefix + " ")

        ret = [original[heading_pos]]
        candidate = original[heading_pos + 1:]

        for x in candidate:
            # print("can ", x, "|", stop_symbol_prefix + "|")
            is_break = False
            for y in stop_symbol_data:
                if x.startswith(y) and len(x) > len(y):
                    is_break = True
                    break

            if is_break:
                break
            else:
                ret.append(x)
    else:
        print("[ERROR] not found heading", block_heading_text)
        raise RuntimeError("Error when processing block text by heading.")

    return ret


def resolve_markdown_link(filepath: str):
    """
    if matched link is in markdown format, extract the real path
    e.g. [describe](real path)
    """
    if filepath is None:
        return None

    if filepath.startswith("[") and filepath.endswith(")") \
            and "](" in filepath:
        total_len = len(filepath)
        pos = filepath.find("](")
        # print(total_len, pos)
        # print(filepath[pos + 2:total_len - 1])
        return filepath[pos + 2:total_len - 1]
    else:
        return filepath


def resolve_wiki_link(filepath: str):
    """
    if matched link is in wiki format, extract the real path
    e.g. [[real path#headers|describe]]
    headers and describe are optional
    """
    if filepath is None:
        return None, None, None

    if filepath.startswith("[[") and filepath.endswith("]]"):
        # print("[resolve_wiki_link] filepath", filepath)
        total_len = len(filepath)
        heading_pos = filepath.find("#")
        display_text_pos = filepath.find("|")
        real_filename = None
        heading_text = None
        display_text = None

        if heading_pos > -1 and display_text_pos > -1 and heading_pos > display_text_pos:
            print("Heading must before display text in wiklink for INCLUDE")
            raise RuntimeError("Error when processing wikilink in INCLUDE" + filepath)

        if heading_pos == -1 and display_text_pos == -1:
            # no heading and no display text
            real_filename = filepath[2:total_len - 2]
        elif heading_pos > -1 and display_text_pos == -1:
            # with heading, no display text
            real_filename = filepath[2:heading_pos]
            heading_text = filepath[heading_pos + 1: total_len - 2]
        elif heading_pos > -1 and display_text_pos > -1:
            # with heading and display text
            real_filename = filepath[2: heading_pos]
            heading_text = filepath[heading_pos + 1: display_text_pos]
            display_text = filepath[display_text_pos + 1: total_len - 2]
        else:
            # no heading, with display text
            real_filename = filepath[2: display_text_pos]
            display_text = filepath[display_text_pos + 1: total_len - 2]

        # print("[resolve_wiki_link]", real_filename, " | ", heading_text, " | ", display_text)

        return real_filename, heading_text, display_text

    else:
        return filepath, None, None


class Include(Module):
    """
    Module for recursively including the contents of other files into the
    current document using a command like `!INCLUDE "path/to/filename"`.
    Target paths can be absolute or relative to the file containing the command
    """

    # matches !INCLUDE directives in .m.md files
    includere = re.compile(r"^!INCLUDE\s+(?:\"([^\"]+)\"|'([^']+)')"
                           r"\s*(?:,\s*(\d+))?\s*$")

    # matches title lines in Markdown files
    titlere = re.compile(r"^(:?#+.*|={3,}|-{3,})$")

    # matches unescaped formatting characters such as ` or _
    formatre = re.compile(r"[^\\]?[_*`]")

    # includes should happen before anything else
    priority = 1

    def transform(self, data):
        transforms = []
        linenum = 0

        for line in data:
            match = self.includere.search(line)
            if match:
                includedata = self.include(match)
                transform = Transform(linenum=linenum, oper="swap",
                                      data=includedata)
                transforms.append(transform)
            linenum += 1

        return transforms

    def include_file(self, filename, pwd="", shift=0, block_heading_text=None, block_display_text=None):
        try:
            f = open(filename, "r", encoding='UTF-8')
            original = f.readlines()
            f.close()

            # fitler by excerpt
            transforms = skip_header_metadata.transform(original)
            if transforms is None:
                pass
            else:
                transformed_data = []
                for transform in transforms:
                    if transform.oper == "noop":
                        transformed_data.append(original[transform.linenum])
                if len(transformed_data) > 0:
                    original = transformed_data

            # filter by block_heading_text
            if block_heading_text is not None:
                original = filter_by_block_heading_text(original, block_heading_text)

            # filter by skip block markers
            inlcudebeginnum = 0
            inlcudebeginsearch = 0
            for line in original:
                stripped = line.strip()
                if stripped == Markers.markup_markdown_begin:
                    inlcudebeginnum = inlcudebeginsearch + 1
                    break
                else:
                    inlcudebeginsearch = inlcudebeginsearch + 1

            data = original[inlcudebeginnum:]

            # line by line, apply shift and recursively include file data
            linenum = 0
            includednum = 0
            for line in data:
                if line.strip() == Markers.markup_markdown_end:
                    return data[:linenum]

                match = self.includere.search(line)
                if match:
                    dirname = path.dirname(filename)
                    data[linenum:linenum + 1] = self.include(match, dirname)
                    includednum = linenum
                    # Update line so that we won't miss a shift if
                    # heading is on the 1st line.
                    line = data[linenum]

                if shift:

                    titlematch = self.titlere.search(line)
                    if titlematch:
                        to_del = []
                        for _ in range(shift):
                            # Skip underlines with empty above text
                            # or underlines that are the first line of an
                            # included file
                            prevtxt = re.sub(self.formatre, '',
                                             data[linenum - 1]).strip()
                            isunderlined = prevtxt and linenum > includednum
                            if data[linenum][0] == '#':
                                data[linenum] = "#" + data[linenum]
                            elif data[linenum][0] == '=' and isunderlined:
                                data[linenum] = data[linenum].replace("=", '-')
                            elif data[linenum][0] == '-' and isunderlined:
                                data[linenum] = '### ' + data[linenum - 1]
                                to_del.append(linenum - 1)
                        for l in to_del:
                            del data[l]

                linenum += 1

            return data

        except (IOError, OSError) as exc:
            print(exc)

        return []

    def include(self, match, pwd=""):
        # file name is caught in group 1 if it's written with double quotes,
        # or group 2 if written with single quotes
        fileglob = match.group(1) or match.group(2)
        # print("include fileglob", fileglob)
        shift = int(match.group(3) or 0)

        fileglob = resolve_markdown_link(fileglob)
        fileglob, heading_text, display_text = resolve_wiki_link(fileglob)

        result = []
        fileglob_path = None

        if pwd != "":
            fileglob_path = path.join(pwd, fileglob)
        else:
            fileglob_path = fileglob

        files = sorted(glob.glob(fileglob_path))

        # One more attempt with ext
        if len(files) == 0 and not fileglob_path.endswith(".md"):
            fileglob_path = path.join(pwd, fileglob + ".md")
            files = sorted(glob.glob(fileglob_path))

        if len(files) == 0:
            print("[WARN] INCLUDE find no file <<" + fileglob + ">>")

        if len(files) > 0:
            for filename in files:
                result += self.include_file(filename, pwd, shift, heading_text, display_text)
        else:
            result.append("")

        return result
