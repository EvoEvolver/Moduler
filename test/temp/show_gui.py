import evonote
from evonote.transform.module_to_tree import get_tree_for_module
import testing_module_multi

tree = get_tree_for_module(testing_module_multi)
tree.show_tree_gui_old()