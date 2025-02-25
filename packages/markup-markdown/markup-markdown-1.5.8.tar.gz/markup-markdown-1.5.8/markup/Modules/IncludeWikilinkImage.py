# -*- coding: utf-8 -*-
# Copyright (C) 2023 Hai Liang W.
# Licensed under the MIT license

import os
from markup.Module import Module
from markup.Transform import Transform

# Get ENV
ENVIRON = os.environ.copy()

MARKUP_WIKILINK_IMAGE_DEFAULT_STYLE = ENVIRON.get("MARKUP_WIKILINK_IMAGE_DEFAULT_STYLE", "width=600px")


def get_markdown_image_link_from_wikilink(wikilink: str):
    '''
    Get markdown image link
    '''
    body = wikilink[3: len(wikilink) - 2]

    image_src = body
    image_caption = ""
    image_style = MARKUP_WIKILINK_IMAGE_DEFAULT_STYLE

    if "|" in body:
        image_src = body[0: body.find("|")]
        image_caption = body[body.rfind("|") + 1:]
        if body.count("|") > 1:
            # extract options
            image_style = body[body.find("|") + 1: body.rfind("|")]

    return "\n![%s](%s){ %s }\n" % (image_caption, image_src, image_style)


class IncludeWikilinkImage(Module):
    """
    Module for including the image link in wiki format
    `![[image.png|caption]]`.
    https://github.com/hailiang-wang/markup-markdown/issues/5
    """
    # include urls should happen after includes
    priority = 1.6

    def transform(self, data):
        transforms = []
        linenum = 0

        for line in data:
            stripped = line.strip()
            if stripped.startswith("![[") and stripped.endswith("]]"):
                stripped = stripped.replace("丨", "|")
                stripped = stripped.replace("｜", "|")
                markdown_image_link = get_markdown_image_link_from_wikilink(stripped)
                transform = Transform(linenum, "swap", markdown_image_link)
                transforms.append(transform)
            linenum = linenum + 1

        return transforms
