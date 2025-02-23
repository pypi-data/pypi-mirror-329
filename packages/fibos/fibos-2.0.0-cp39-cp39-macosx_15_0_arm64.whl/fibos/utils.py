# fibos/utils.py
import os
import platform
from ctypes import CDLL

def _load_library(name):
    package_dir = os.path.abspath(os.path.dirname(__file__))
    if platform.system() == 'Windows':
        lib_name = f'{name}.dll'
    elif platform.system() == 'Darwin':
        lib_name = f'{name}.dylib'
    else:
        lib_name = f'{name}.so'
    lib_path = os.path.join(package_dir, lib_name)
    if not os.path.exists(lib_path):
        raise ImportError(f"Library not found: {lib_path}")
    return CDLL(lib_path)
