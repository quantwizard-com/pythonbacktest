# this code will help importing strategies from external files
# which isn't very easy in Python for some reason

import imp

def import_strategy(module_name, full_path):
    return imp.load_source(module_name, full_path)