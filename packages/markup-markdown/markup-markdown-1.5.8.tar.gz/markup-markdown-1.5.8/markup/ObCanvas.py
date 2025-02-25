#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ===============================================================================
#
# Copyright (c) 2020 <> All Rights Reserved
#
#
# File: /c/Users/Administrator/git/markup-markdown/markup/ObCanvas
# Author: Hai Liang Wang
# Date: 2023-03-09:06:41:55
#
# ===============================================================================

"""
Process Obsidian Canvas into Markup Markdown
Help: https://github.com/hailiang-wang/markup-markdown/issues/9
"""
__copyright__ = "Copyright (c) 2023 . All Rights Reserved"
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

import json
from copy import deepcopy
from datetime import datetime

# Get ENV
ENVIRON = os.environ.copy()
EXCERPT_PAGE_TITLE = ENVIRON.get("EXCERPT_PAGE_TITLE", "").strip()
EXCERPT_URL = ENVIRON.get("EXCERPT_URL", "").strip()
EXCERPT_LANG = ENVIRON.get("EXCERPT_LANG", "cn").strip()
EXCERPT_TAGS = ENVIRON.get("EXCERPT_TAGS", "pipeline,index").strip()


def get_tags_from_env():
    '''
    Get tags from ENV
    '''
    tags = set()

    for x in EXCERPT_TAGS.split(","):
        x = x.strip()
        if x:
            tags.add(x)

    return list(tags)


def get_card_from_canvas_raw_data(canvas_raw_data, card_text="root"):
    '''
    Get root node
    '''
    for node in canvas_raw_data["nodes"]:
        if node["type"] == "text":
            text = node["text"].lower()
            if text == card_text:
                return node


def qualify(canvas_raw_data):
    '''
    Check nodes for root node
    '''
    ret = True
    # check nodes and edges exist
    canvas_raw_keys = canvas_raw_data.keys()
    if ("nodes" not in canvas_raw_keys) or ("edges" not in canvas_raw_keys):
        print("[qualify] Invalid data of Canvas file")
        return False

    # check root node exist
    roots = []
    for node in canvas_raw_data["nodes"]:
        if node["type"] == "text":
            text = node["text"].lower()
            if text == "root":
                roots.append(node)
    if len(roots) != 1:
        print("Invalid canvas data, root node as card must exist *1*, current %s" % len(roots))
        return False

    return ret


def get_node_by_id(canvas_raw_data, node_id):
    '''
    Get node by id
    '''
    for node in canvas_raw_data["nodes"]:
        if node["id"] == node_id:
            return deepcopy(node)

    raise RuntimeError("Node %s not exist" % node_id)


def get_children_of_node(canvas_raw_data, parent_node):
    '''
    Get children from node,
    Parent: `fromNode`, send the arrow
    Child: `toNode`, receive the arrow
    '''
    children = []

    for edge in canvas_raw_data["edges"]:
        if edge["fromNode"] == parent_node["id"]:
            if edge["toNode"] not in children:
                node = get_node_by_id(canvas_raw_data, edge["toNode"])
                node["edge"] = deepcopy(edge)
                node["children"] = get_children_of_node(canvas_raw_data, node)
                children.append(node)

    # sort children
    if len(children) > 1:
        # the upper in the Y axis, the topper of list
        children = sorted(children, key=lambda x: x["y"])

    return children


def canvas2dicttree(canvas_raw_data, root_node):
    '''
    Convert canvas dict into tree layout
    '''
    root = get_card_from_canvas_raw_data(canvas_raw_data=canvas_raw_data, card_text=root_node)
    # print("root", root)

    root_children = get_children_of_node(canvas_raw_data, root)
    # print("children", json.dumps(root_children, indent=2, ensure_ascii=False))

    return root_children


def find_obsidian_vault_rootdir(check_path):
    """
    find obsidian vault root dir
    """
    if not os.path.exists(check_path):
        return None

    if os.path.exists(os.path.join(check_path, ".obsidian")):
        return check_path

    return find_obsidian_vault_rootdir(os.path.dirname(check_path))


def parse_edge_labels(edge):
    '''
    Get label as dict, all key or flag are in lowercase.
    values are all trimed.
    '''
    atts = dict()

    if "label" in edge:
        splits = [x.strip() for x in edge["label"].split("\n")]
        for x in splits:
            if "=" in x and not x.startswith("="):
                ys = [y.strip() for y in x.split("=", 1)]
                if len(ys) == 2:
                    atts[ys[0].lower()] = ys[1]
                else:
                    atts[ys[0].lower()] = True
            else:
                atts[x.lower()] = True

    # print("[parse_edge_labels]", atts)

    return atts


def append_content_with_tree_branch(content: list, branch, vault_root_dir, output_path):
    '''
    Append content with Tree branch
    '''
    # print("[append_content_with_tree_branch] id %s, type %s" % (branch["id"], branch["type"]))
    atts = parse_edge_labels(branch["edge"])

    if "ap_former_page_break_no" in atts:
        pass
    else:
        content.append("\n<!-- markup:page-break-xml -->\n")

    if branch["type"] == "text":
        content.append(branch["text"])
        content.append("\n")

        if "ap_tail_page_break_no" in atts:
            content.append("\n<!-- markup:page-break-xml -->\n")
    elif branch["type"] == "file":
        append_headings = atts["ap_heading_level"] if "ap_heading_level" in atts else "1"
        file_path = branch["file"]

        file_abs_path = os.path.join(vault_root_dir, file_path)
        file_rel_path = os.path.relpath(file_abs_path, os.path.dirname(output_path))

        if append_headings and append_headings.isdigit():
            content.append('''!INCLUDE "[[%s]]", %s ''' % (file_rel_path, append_headings))
        else:
            content.append('''!INCLUDE "[[%s]]"''' % (file_rel_path))

        content.append("\n")

        if "ap_tail_page_break_no" not in atts:
            content.append("\n<!-- markup:page-break-xml -->\n")

    if "children" in branch and len(branch["children"]) > 0:
        for x in branch["children"]:
            content = append_content_with_tree_branch(content, x, vault_root_dir, output_path)

    return content


def dicttree2markupmarkdown(tree, output_file):
    '''
    Dict tree data to markup markdown file
    '''
    output_path = os.path.join(os.getcwd(), output_file)
    default_date = datetime.today().strftime('%Y-%m-%d')
    default_tags = json.dumps(get_tags_from_env(), ensure_ascii=False)
    default_title = EXCERPT_PAGE_TITLE
    default_url = EXCERPT_URL
    default_lang = EXCERPT_LANG
    content = ['''---
date: %s
#mindmap-plugin: basic
tags: %s
page-title: "%s"
url: %s
---

<!-- CAUTION: THIS FILE IS GENERATED WITH `canvas` COMMAND AUTOMATICALLY -->
<!--          JUST STAY WITH THE CANVAS!!! ANY CHANGES MADE IN THIS FILE DIRECTLY MAY LOSE.-->
<!-- Help Guide of Markup Markdown, https://github.com/hailiang-wang/markup-markdown -->
<!-- Cover xxx.cover.doc -->

<!-- generate toc and section in headers -->
!TOC 5 %s section_only

''' % (
        default_date,
        default_tags,
        default_title,
        default_url,
        default_lang
    )]

    vault_root_dir = find_obsidian_vault_rootdir(os.getcwd())
    print(">> Work against Obsidian Vault", vault_root_dir)

    for branch in tree:
        content = append_content_with_tree_branch(content, branch, vault_root_dir=vault_root_dir, output_path=output_path)

    with open(output_path, "w", encoding="utf-8") as fout:
        fout.writelines(content)
        print(">> Saved output %s" % output_path)


def canvas2markup(input_file, output_file, root_node):
    '''
    Canvas to markup
    '''
    print(">> Canvas2markup <<INPUT %s >>OUTPUT %s" % (input_file, output_file))
    canvas_raw_data = dict()
    with open(input_file, "r", encoding="utf-8") as fin:
        canvas_raw_data = json.load(fin)

    if qualify(canvas_raw_data):
        # build output tree
        tree = canvas2dicttree(canvas_raw_data=canvas_raw_data, root_node=root_node)

        # save tree into output markdown
        dicttree2markupmarkdown(tree, output_file)
    else:
        raise RuntimeError("[canvas2markup] Error")


def handle(args):
    """
    Convert Obsidian Canvas to Markup Markdown
    """
    input_file = args.input
    output_file = args.output
    action_type = args.action
    root_node = args.root

    if not input_file or not os.path.exists(input_file):
        raise RuntimeError("Invalid params input, None or not found %s" % input_file)

    if not output_file or os.path.exists(output_file):
        raise RuntimeError("Invalid params output, None or exist %s" % output_file)

    if action_type == "canvas2markup":
        canvas2markup(input_file=input_file, output_file=output_file, root_node=root_node)
