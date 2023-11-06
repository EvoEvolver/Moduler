from __future__ import annotations

import inspect


def get_source(obj):
    try:
        return inspect.getsource(obj)
    except:
        return ""


def get_docs(obj) -> str | None:
    return obj.__doc__


def get_file(obj) -> str | None:
    try:
        return inspect.getfile(obj)
    except:
        print(obj.__name__)
        print("get file failed")
        return None


def get_member_pos(member) -> tuple[int, int] | None:
    try:
        struct_src, struct_start_line = inspect.getsourcelines(member)
        struct_end_line = struct_start_line + len(struct_src)
        pos = (struct_start_line, struct_end_line)
        return pos
    except:
        return None
