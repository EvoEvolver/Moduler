import yaml

# open testing_module_multi/.tree.yml
with open("../testing_module_multi/.tree.yml", "r") as f:
    tree = yaml.load(f, Loader=yaml.FullLoader)
print(tree)