from __future__ import annotations

import importlib
import inspect
import os
import pkgutil
from types import BuiltinFunctionType
from typing import List, Dict

import yaml

from moduler import Struct
from moduler.comment_parser import prepare_raw_comment_struct, parse_raw_comments
from moduler.utils import get_source, get_file, get_member_pos


def build_module_tree(module) -> Struct:
    root_path = module.__file__.split("__init__.py")[0]
    module_struct, sub_modules = extract_module_tree_without_comment(module, root_path)
    sub_modules: Dict[str, Struct] | List[Struct]

    module_src = get_source(module)

    # Extract the three quote comments in the module
    raw_comment_struct_list = prepare_raw_comment_struct(module_src)

    # Mix the comments and functions and classes into a list of Struct sorted by the start line.
    add_raw_comments_to_struct(raw_comment_struct_list, module_struct)

    # Parse the raw comments into Structs
    parse_raw_comments(module_struct)

    # Build the section tree from a flat list of Structs
    build_section_tree(module_struct)

    # Process the sub_modules
    process_sub_modules(sub_modules, module_struct)

    # Add the readme to the module_struct if exists
    add_readme(module_struct, root_path)

    return module_struct


"""
# Extract the tree or module without processing comments
"""


def extract_module_tree_without_comment(module, root_path):
    module_struct: Struct = Struct("module", module, None, module.__name__)

    sub_modules = get_sub_module_list_or_dict(module)

    true_member_names, true_members = extract_module_members(module, root_path)

    extract_function_and_example_and_todo(module_struct, true_member_names, true_members)

    return module_struct, sub_modules


"""
## Extract sub-modules
"""


def get_sub_module_list_or_dict(module):
    # Get the sub_modules
    sub_modules = get_direct_sub_modules(module)
    # Get sub_module tree from .tree.yml if it exists
    module_dir = os.path.dirname(inspect.getfile(module))
    tree_yml_path = os.path.join(module_dir, ".tree.yml")
    tree_config_dict = {}
    if os.path.exists(tree_yml_path):
        try:
            with open(tree_yml_path, "r") as f:
                tree_config_dict = yaml.load(f, Loader=yaml.FullLoader)
        except:
            pass
    if module.__file__.endswith("__init__.py") and len(tree_config_dict) > 0:
        sections_dict = build_module_section_dict(tree_config_dict, sub_modules)
        if sections_dict is not None:
            sub_modules = sections_dict
    return sub_modules


def get_direct_sub_modules(module):
    module_dir = os.path.dirname(inspect.getfile(module))
    sub_modules = []
    is_pkg = hasattr(module, "__path__")
    if is_pkg:
        for sub_module_info in pkgutil.iter_modules([module_dir]):
            sub_module = importlib.import_module(
                module.__name__ + "." + sub_module_info.name)
            sub_modules.append(sub_module)
    return sub_modules


def build_module_section_dict(tree_config_dict, sub_modules):
    if "sections" not in tree_config_dict:
        return None
    sections_dict = tree_config_dict["sections"]
    if len(sections_dict) == 0:
        return
    sections_dict: Dict
    name_to_module = {}
    for sub_module in sub_modules:
        name = sub_module.__name__.split(".")[-1]
        name_to_module[name] = sub_module
    map_module_name_to_module(sections_dict, name_to_module)
    if len(name_to_module) > 0:
        default_section_title = tree_config_dict.get("default section", "Others")
        sections_dict[default_section_title] = list(name_to_module.values())
    return sections_dict


def map_module_name_to_module(sections_dict: Dict, name_to_module: Dict):
    """
    Recursively map the module name to module. Delete the module name from name_to_module in the process.
    The module that is not map remains in name_to_module.
    In the result, the leaf elements can be module, str, or None.
    The str elements are the docstrings of the section
    The None elements are the module not found
    """
    for title, content_list in sections_dict.items():
        for i, content in enumerate(content_list):
            if isinstance(content, str):
                if content in name_to_module:
                    content_list[i] = name_to_module[content]
                    del name_to_module[content]
                else:
                    if i == 0:
                        pass
                    else:
                        content_list[i] = None
            elif isinstance(content, dict):
                map_module_name_to_module(content, name_to_module)


"""
## Extract function, class, todo and examples in the module
"""


def extract_module_members(module, root_path):
    # Get the classes and functions
    true_members = []
    true_member_names = []
    for name in dir(module):
        member = module.__dict__[name]
        # check the type of the member is in module, class, method, function
        if (str(type(member)) not in ["<class 'type'>",
                                      "<class 'function'>"]):
            continue
        if isinstance(member, BuiltinFunctionType):
            continue

        member_path = get_file(member)
        if member_path is None:
            continue

        # skip the members defined outside the root path
        if member_path != root_path:
            continue
        true_members.append(member)
        true_member_names.append(name)
    return true_member_names, true_members


def extract_function_and_example_and_todo(module_struct, member_names, members):
    n_todo = 1
    for i, member in enumerate(members):
        name = member_names[i]
        pos = get_member_pos(member)
        if pos is None:
            continue
        parent_struct = module_struct
        # check decorators
        if hasattr(member, "__moduler_todo"):
            member_type = "function" if inspect.isfunction(member) else "class"
            todo_struct = Struct("todo", member.__moduler_todo, pos,
                                 f"{member_type}: {member.__name__}")
            n_todo += 1
            module_struct.children.append(todo_struct)
            parent_struct = todo_struct
        elif hasattr(member, "__moduler_example") and member.__moduler_example:
            example_struct = Struct("example", None, pos, member.__name__)
            module_struct.children.append(example_struct)
            parent_struct = example_struct

        add_function_class_to_struct(member, parent_struct, name, pos)


def add_function_class_to_struct(member, parent_struct, name, pos):
    if inspect.isclass(member):
        class_struct = Struct("class", member, pos, name)
        extract_class_struct_without_comment(class_struct, member)
        parent_struct.children.append(class_struct)
    elif inspect.isfunction(member):
        parent_struct.children.append(Struct("function", member, pos, name))


def extract_class_struct_without_comment(class_struct, class_):
    for name, member in inspect.getmembers(class_):
        if isinstance(member, classmethod):
            continue
        type_str = str(type(member))
        # check whether member is a function
        if type_str == "<class 'function'>":
            pos = get_member_pos(member)
            # check whether the function is from parent class
            if member.__qualname__.split(".")[0] != class_.__name__:
                continue
            class_struct.children.append(Struct("function", member, pos, name))
        # Add classmethods
        elif type_str == "<class 'mappingproxy'>":
            for sub_name, sub_member in member.items():
                if isinstance(sub_member, classmethod):
                    pos = get_member_pos(sub_member)
                    class_struct.children.append(
                        Struct("function", sub_member, pos, name))


"""
# Use comments to build the section tree
"""
"""
## Add raw comments to the struct
"""


def add_raw_comments_to_struct(cmt_structs: List[Struct], root_struct: Struct):
    """
    Mix the comment_structs and cls_func_structs into a list of struct
    :param cmt_structs: The comment_structs
    :param cls_func_structs: The cls_func_structs
    :return: A list of struct sorted by the start line
    """
    cls_func_structs = root_struct.children

    # sort cls_func_structs by the start line
    cls_func_structs.sort(key=lambda x: x.pos[0])

    structs: List[Struct] = []
    cmt_index = 0
    cls_func_index = 0

    while cmt_index < len(cmt_structs) and cls_func_index < len(cls_func_structs):
        next_cmt = cmt_structs[cmt_index]
        next_cls_func = cls_func_structs[cls_func_index]
        # If the comment ends before next function or class
        # It can be added because we have skipped all the comments inside functions and classes
        if next_cmt.pos[1] < next_cls_func.pos[0]:
            structs.append(next_cmt)
            cmt_index += 1
        # If the comment end after the start of the next function or class, it might be inside of it, or after
        # We need to add the struct of the function or class first and then check whether the comment is inside
        else:
            structs.append(next_cls_func)
            curr_cls_func_end = next_cls_func.pos[1]
            cls_func_index += 1

            covered_comments = []
            while cmt_index < len(cmt_structs):
                cmt_end = cmt_structs[cmt_index].pos[1]
                if cmt_end < curr_cls_func_end:
                    covered_comments.append(cmt_structs[cmt_index])
                    cmt_index += 1
                else:
                    break
            if next_cls_func.struct_type == "class":
                add_raw_comments_to_struct(covered_comments, next_cls_func)

    # append the remaining comment_structs
    if (len(structs) > 0 and cmt_index < len(cmt_structs)
            and cmt_structs[cmt_index].pos[0] >= cls_func_structs[-1].pos[1]):
        structs.extend(cmt_structs[cmt_index:])
    # append the remaining cls_func_structs
    if cls_func_index < len(cls_func_structs):
        structs.extend(cls_func_structs[cls_func_index:])
    if len(cls_func_structs) == 0:
        structs.extend(cmt_structs[cmt_index:])

    root_struct.children = structs


"""
## Build section tree by processing section headers in comments
"""


def build_section_tree(root_struct: Struct):
    section_level_stack = [-1]
    parent_list = [root_struct]
    original_children = root_struct.children
    root_struct.children = []

    n_comment = 1
    for struct in original_children:
        struct_type = struct.struct_type
        struct_obj = struct.obj
        curr_parent = parent_list[-1]
        if struct_type == "comment":
            curr_parent.children.append(
                Struct("comment", struct_obj, None, None))
        elif struct_type == "section":
            section_title, section_level = struct_obj
            struct.name = section_title
            curr_section_level = section_level_stack[-1]
            if section_level > curr_section_level:
                section_level_stack.append(section_level)
            elif section_level < curr_section_level:
                while section_level_stack[-1] >= section_level:
                    section_level_stack.pop()
                    parent_list.pop()
                section_level_stack.append(section_level)
            else:
                parent_list.pop()
            parent_list[-1].children.append(struct)
            parent_list.append(struct)
        elif struct_type == "class":
            build_section_tree(struct)
            parent_list[-1].children.append(struct)
        else:
            parent_list[-1].children.append(struct)

    return root_struct


def process_sub_modules(sub_modules: List | Dict, root_struct: Struct):
    if isinstance(sub_modules, list):
        process_sub_modules_in_list(root_struct, sub_modules)
    elif isinstance(sub_modules, dict):
        process_sub_modules_in_dict(root_struct, sub_modules)
    else:
        assert False


def process_sub_modules_in_list(root_struct: Struct, sub_modules: List):
    for i, sub_module in enumerate(sub_modules):
        if isinstance(sub_module, dict):
            process_sub_modules(sub_module, root_struct)
        elif isinstance(sub_module, str):
            root_struct.children.append(Struct("comment", sub_module, None, None))
        elif sub_module is not None:
            root_struct.children.append(build_module_tree(sub_module))


def process_sub_modules_in_dict(root_struct: Struct, sub_modules: Dict):
    for title, sub_module_list in sub_modules.items():
        if root_struct.struct_type == "section":
            new_level = root_struct.obj[1] + 1
            new_section = Struct("section", (title, new_level), None, title)
            process_sub_modules(sub_module_list, new_section)
        else:
            new_section = Struct("section", (title, 1), None, title)
            process_sub_modules(sub_module_list, new_section)
        root_struct.children.append(new_section)


"""
# Extract the readme
"""


def add_readme(module_struct, root_path):
    readme = extract_readme(root_path)
    if readme is not None:
        readme_struct = Struct("document", readme, None, "README")
        module_struct.children.insert(0, readme_struct)


def extract_readme(module_dir):
    readme_path = os.path.join(module_dir, "README.md")
    if not os.path.exists(readme_path):
        return None
    with open(readme_path, "r") as f:
        readme = f.read()
    return readme
