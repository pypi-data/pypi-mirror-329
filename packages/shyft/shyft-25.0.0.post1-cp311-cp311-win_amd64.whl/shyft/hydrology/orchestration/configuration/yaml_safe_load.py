import importlib
import yaml

def shyft_class_constructor(loader, tag_suffix: str, node):
    """Add the possibility to import a class name from shyft
    
    Example:
        Read `!!python/name:shyft.time_series._time_series.Calendar ''` 
        will be a class <class 'shyft.time_series._time_series.Calendar'>
    """
    # get the name of the class or object from the node value
    if not tag_suffix.startswith("shyft."):
        raise NotImplementedError("Only loading shyft classes is supported")
    if not node.value == "":
        raise NotImplementedError("Can only load class names, not initialize them")
    # split the name by dot and get the module and attribute names
    module_name, attr_name = tag_suffix.rsplit(".", 1)
    # import the module and get the attribute
    module = importlib.import_module(module_name)
    attr = getattr(module, attr_name)
    # return the attribute as the constructed object
    return attr

# register the constructor for !!python/name
yaml.add_multi_constructor("tag:yaml.org,2002:python/name:", shyft_class_constructor, Loader=yaml.SafeLoader)