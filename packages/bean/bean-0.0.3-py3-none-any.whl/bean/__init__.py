import os, sys

def load_my_library(lib_name, path_template="/projects/{lib_name}/source/src"):
    lib_abs_path = os.path.expandvars("$HOME") + path_template.format(lib_name=lib_name)
    if lib_abs_path not in sys.path:
        sys.path.insert(0, lib_abs_path)
        return True
    return False
