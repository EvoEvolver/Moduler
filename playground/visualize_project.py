from moduler.core import build_module_tree
from moduler.gui import draw_treemap
import moduler

struct = build_module_tree(moduler)
draw_treemap(struct)