from moduler import Struct
import plotly.graph_objects as go
import inspect
from moduler.core import build_module_tree

def draw_module_tree():
    # Get current module by inspecting the stack
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    struct = build_module_tree(module)
    draw_treemap(struct)


"""
## Draw treemap
"""

def draw_treemap(struct: Struct):
    ids, labels, parents, texts = extract_tree_ingredients(struct)
    texts = [hypenate_texts(text) for text in texts]
    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        # values=values,
        ids=ids,
        text=texts,
        # text=values,
        root_color="lightgrey",
        # hoverinfo="label+text",
        # hovertemplate="<b>%{label}</b><br>%{hovertext}",
        texttemplate="<b>%{label}</b><br>%{text}",
        hovertemplate="<b>%{label}</b><br>%{text}<extra></extra>",
        hoverinfo="text",
        # marker=dict(cornerradius=5)
    ))

    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    # fig.update_traces(marker=dict(cornerradius=5))
    fig.show()


"""
## Extract tree ingredients for treemap visualization
"""

def extract_tree_ingredients(root: Struct):
    labels = []
    parents = []
    texts = []
    ids = []
    add_ingredients_to_lists(root, root.name, 0, labels, parents, texts, ids)
    return ids, labels, parents, texts

def add_ingredients_to_lists(root: Struct, root_path: str, root_idx: int, labels, parents, texts, ids):
    n_sections = 0
    for child in root.children:
        if child.struct_type == "comment":
            texts[root_idx] += child.obj
            continue
        labels.append(child.name)
        parents.append(root_path)
        if child.struct_type in "section":
            n_sections += 1
            child_name = child.struct_type + " " + str(n_sections) + ". " + child.name
        else:
            child_name = child.struct_type + " " + child.name
        child_path = root_path + child_name + "/"
        ids.append(child_path)
        if child.struct_type == "section":
            texts.append(child.name)
            add_ingredients_to_lists(child, child_path, len(texts)-1, labels, parents, texts, ids)
        elif child.struct_type == "module":
            texts.append("")
            add_ingredients_to_lists(child, child_path, len(texts)-1, labels, parents, texts, ids)
        elif child.struct_type == "class":
            texts.append("")
            add_ingredients_to_lists(child, child_path, len(texts)-1, labels, parents, texts, ids)
        elif child.struct_type == "function":
            texts.append("")
            add_ingredients_to_lists(child, child_path, len(texts)-1, labels, parents, texts, ids)
        elif child.struct_type == "document":
            texts.append(child.obj)
            add_ingredients_to_lists(child, child_path, len(texts) - 1, labels, parents,
                                     texts, ids)
        else:
            raise



"""
## Hypenate texts
"""

from hyphen import Hyphenator
from hyphen.textwrap2 import fill

h_en = Hyphenator('en_US')


def hypenate_texts(texts: str, line_width=40):
    """
    Hypenate texts. Add <br> to the end of each line.
    :param texts: The texts to be hypenated
    :param line_width: The width of each line
    :return: The hypenated texts
    """
    if "\\" in texts:
        hyphenator = False
    else:
        hyphenator = h_en
    try:
        texts = fill(texts, width=line_width, use_hyphenator=hyphenator)
    except:
        texts = fill(texts, width=line_width, use_hyphenator=False)
    texts = texts.replace("\n", "<br>")
    return texts


if __name__ == '__main__':
    import moduler
    struct = build_module_tree(moduler)
    draw_treemap(struct)