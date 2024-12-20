from __future__ import annotations

import re
from typing import List

from moduler import Struct
import ast
from typing import Union

"""
This module is for parse and extract comments
"""

def extract_comments(root_node: Union[ast.Module, ast.ClassDef]):
    res = []
    string_nodes = []
    class_nodes = []
    for node in root_node.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
            string_nodes.append(node)
            res.append(node)
        elif isinstance(node, ast.ClassDef):
            class_nodes.append(node)
            class_res = extract_comments(node)
            res.extend(class_res)
    return res

def extract_comments_from_str(src: str):
    tree = ast.parse(src)
    return extract_comments(tree)


def prepare_raw_comment_struct(parent_src: str) -> List[Struct]:
    nodes = extract_comments_from_str(parent_src)
    comment_struct_list = []
    for node in nodes:
        comment_pos = (node.lineno, node.end_lineno)
        comment_struct_list.append(Struct("raw_comment", node.value.s, comment_pos))
    return comment_struct_list


def get_min_pos_for_line(src: str) -> List[int]:
    src_lines = src.split("\n")
    min_pos_for_line = [0]
    for line in src_lines:
        min_pos_for_line.append(min_pos_for_line[-1] + len(line) + 1)
    return min_pos_for_line


def find_line_no(pos: int, min_line_no, min_pos_for_line: List[int]) -> int:
    for i in range(min_line_no - 1, len(min_pos_for_line)):
        if pos < min_pos_for_line[i]:
            return i


section_pattern = re.compile(r"(\n\s*?#+ .*)")


def parse_raw_comments(root_struct: Struct):
    new_children = []
    for i, struct in enumerate(root_struct.children):
        if struct.struct_type == "raw_comment":
            comment_content = struct.obj
            comment_structs = process_raw_comment_content(comment_content)
            new_children.extend(comment_structs)
        else:
            new_children.append(struct)
            if struct.struct_type == "class":
                parse_raw_comments(struct)
    root_struct.children = new_children


def process_raw_comment_content(comment_content: str) -> List[Struct]:
    min_pos_for_line = get_min_pos_for_line(comment_content)
    min_line_no = 1

    structs_in_comment = []
    # Find all sections which should start with one or more # followed by a space
    section_matches = section_pattern.finditer(comment_content)
    last_section_end = 0
    for section_match in section_matches:
        section_markdown = section_match.group(1)[1:].lstrip()
        # find first non-# character
        section_title = section_markdown.lstrip("#")
        section_level = len(section_markdown) - len(section_title)
        section_title = section_title.strip()
        section_start, section_end = section_match.span()
        start_line_no = find_line_no(section_start, min_line_no, min_pos_for_line)
        end_line_no = find_line_no(section_end, start_line_no, min_pos_for_line)
        min_line_no = end_line_no
        comment_text_before_section = comment_content[last_section_end + 1:section_start]
        last_section_end = section_end
        if len(comment_text_before_section) > 0:
            structs_in_comment.append(
                Struct("comment", comment_text_before_section, (0, start_line_no)))
        structs_in_comment.append(
            Struct("section", (section_title, section_level),
                   (start_line_no, end_line_no)))
    if last_section_end < len(comment_content):
        remaining_text = comment_content[last_section_end:].strip()
        if len(remaining_text) > 0:
            last_section_end_line_no = find_line_no(last_section_end, min_line_no, min_pos_for_line)
            structs_in_comment.append(Struct("comment", remaining_text,
                                         (last_section_end_line_no, len(min_pos_for_line)-1)))
    return structs_in_comment
