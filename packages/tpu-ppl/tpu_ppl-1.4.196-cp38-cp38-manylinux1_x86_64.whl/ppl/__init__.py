"""isort:skip_file"""
__version__ = '2.1.0'
import os, sys
import subprocess
# ---------------------------------------
# Note: import order is significant here.

if not os.environ.get('PPL_PROJECT_ROOT'):
    current_dir_path = os.path.dirname(os.path.abspath(__file__))
    os.environ['PPL_PROJECT_ROOT'] = os.path.join(current_dir_path, "3rd")
    os.environ['PPL_RUNTIME_PATH'] = os.path.join(current_dir_path, "3rd/runtime")
    os.environ['PPL_THIRD_PARTY_PATH'] = os.path.join(current_dir_path, "3rd/third_party")
    current_path = os.environ.get('PATH', '')
    os.environ['PATH'] = current_path + ":" + os.path.join(current_dir_path, "3rd/bin") \
                         + ":" + os.path.join(current_dir_path, "3rd/python/tool")
    current_path = os.environ.get('PYTHONPATH', '')
    os.environ['PYTHONPATH'] = current_path + ":" + os.path.join(current_dir_path, "3rd/python") \
                               + ":" + current_dir_path

def ensure_package_installed(package_name, version=None, find_links=None, mirror=None):
    try:
        __import__(package_name)
    except ImportError:
        print(f"{package_name} is not installed. Installing...")
        install_command = [sys.executable, "-m", "pip", "install"]
        if version:
            install_command.append(f"{package_name}=={version}")
        else:
            install_command.append(package_name)
        if find_links:
            install_command.extend(["-f", find_links])
        if mirror:
            install_command.extend(["-i", mirror])
        try:
            subprocess.check_call(install_command)
            print(f"{package_name} installed successfully.")
        except subprocess.CalledProcessError as e:
            ver = f"=={version}" if version else ""
            print(f"Failed to install {package_name}{ver}")
            ensure_package_installed(package_name)
            sys.exit(1)

# check numpy torch
ensure_package_installed("numpy", "1.26.2")
ensure_package_installed("torch", "2.1.1+cpu",
                         "https://download.pytorch.org/whl/torch_stable.html")

# submodules
from .runtime import (
    autotune,
    Config,
    heuristics,
    JITFunction,
    KernelInterface,
    OutOfResources,
    MockTensor,
    pl_extension,
    Chip,
    ErrorCode,
)
from .runtime.jit import jit, autotiling
from .compiler import compile, CompilationError

from . import language

__all__ = [
    "autotune",
    "cdiv",
    "CompilationError",
    "compile",
    "Config",
    "heuristics",
    "impl",
    "jit",
    "autotiling",
    "JITFunction",
    "KernelInterface",
    "language",
    "MockTensor",
    "next_power_of_2",
    "OutOfResources",
    "runtime",
    "testing",
    "tool",
    "pl_extension",
    "Chip",
    "ErrorCode",
]

# -------------------------------------
# misc. utilities that  don't fit well
# into any specific module
# -------------------------------------

def cdiv(x: int, y: int):
    return (x + y - 1) // y


def next_power_of_2(n: int):
    """Return the smallest power of 2 greater than or equal to n"""
    n -= 1
    n |= n >> 1
    n |= n >> 2
    n |= n >> 4
    n |= n >> 8
    n |= n >> 16
    n |= n >> 32
    n += 1
    return n
