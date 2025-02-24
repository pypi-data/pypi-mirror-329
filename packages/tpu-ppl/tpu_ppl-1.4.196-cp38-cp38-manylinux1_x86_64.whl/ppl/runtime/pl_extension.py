import os
import torch
import shutil
import subprocess
import functools
from torch.utils.cpp_extension import load
from .ppl_types import Chip
from .cache import LRUCache, default_cache_dir, get_folder_size


def _os_system_log(cmd_str):
    # use subprocess to redirect the output stream
    # the file for saving the output stream should be set if using this function
    print("[Running]: {}".format(cmd_str))

    process = subprocess.run(
        cmd_str,
        shell=True,
        stdin=subprocess.PIPE,
        #  stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True)
    ret = process.returncode
    if ret == 0 and process.stderr.find("error") == -1:
        print("[Success]: {}".format(cmd_str))
    else:
        print(process.stdout)
        print(process.stderr)
        raise RuntimeError("[!Error]: {}".format(cmd_str))


def _os_system(cmd: list, save_log: bool = False, inner_info: bool = True):
    cmd_str = ""
    for s in cmd:
        cmd_str += str(s) + " "
    if not save_log:
        print("[Running]: {}".format(cmd_str))
        if inner_info:
            ret = os.system(cmd_str)
        else:
            process = subprocess.run(cmd_str,
                                     shell=True,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     universal_newlines=True)
            ret = process.returncode
            if "error" in process.stderr.lower():
                print(process.stderr)
                raise RuntimeError("[!Error]: {}".format(cmd_str))
        if ret == 0:
            print("[Success]: {}".format(cmd_str))
        else:
            raise RuntimeError("[!Error]: {}".format(cmd_str))
    else:
        _os_system_log(cmd_str)

def build_code(work_path, file_path, func_name, chip=None, build_debug=False):
    if isinstance(chip, Chip):
        chip_name = chip.str
    elif isinstance(chip, str):
        chip_name = chip
    elif chip is None:
        chip_name = os.getenv("CHIP", default="bm1684x")
    else:
        raise ValueError("chip must be a string or ppl.Chip")
    file_name = os.path.basename(file_path)
    # file_name_without_ext = os.path.splitext(file_name)[0]
    so_name = func_name
    ppl_root = os.environ["PPL_PROJECT_ROOT"]
    cur_dir = os.environ["PWD"]
    build_path = os.path.join(work_path, "build")

    if os.path.exists(work_path):
        shutil.rmtree(work_path)
    os.makedirs(work_path)

    # compile pl file
    cmd = [
        "ppl-compile", file_path, "--print-debug-info", "--print-ir",
        "--chip {}".format(chip_name), "--O2", "--mode=2",
        "--o {}".format(work_path)
    ]
    _os_system(cmd, True)
    cmake_file = os.path.join(ppl_root, "runtime/scripts/torch.cmake")
    shutil.copy(cmake_file, os.path.join(work_path, "CMakeLists.txt"))
    if not os.path.exists(build_path):
        os.mkdir(build_path)
    os.chdir(build_path)
    _os_system([
        "cmake .. -DDEBUG={} -DCHIP={} -DOUT_NAME={}".format(
            build_debug, chip_name, so_name)
    ])
    if build_debug:
        _os_system(["make install VERBOSE=1"])
    else:
        _os_system(["make install"])
        shutil.rmtree(build_path)
    os.chdir(cur_dir)
    return

class pl_extension:
    cache = LRUCache(cache_folde="cxx")
    @cache.register(cache_fn=build_code)
    @staticmethod
    def load(file_path, func_name, chip=None, build_debug=False):
        ppl_root = os.environ["PPL_PROJECT_ROOT"]
        file_name = os.path.basename(file_path)
        file_name_without_ext = os.path.splitext(file_name)[0]
        so_name = func_name
        # open mem check func
        so_path = pl_extension.cache.get_cached_file("lib/lib" + so_name + ".so")
        mem_file = pl_extension.cache.get_cached_file("src/" + file_name_without_ext + "_torch.cpp")
        host_path = pl_extension.cache.get_cached_file("host")
        pl_extension.cache.get_cached_file("device")
        pl_extension.cache.get_cached_file("include")

        include_dir = []
        include_dir.append(os.path.join(ppl_root, "runtime/customize/include"))
        include_dir.append(host_path)
        extra_cflags = []
        if build_debug:
            extra_cflags = ['-g']
        else:
            extra_cflags = ['-O3', '-DNDEBUG']
        module = torch.utils.cpp_extension.load(
            name=func_name + '_check_mem_torch',
            extra_include_paths=include_dir,
            extra_cflags=extra_cflags,
            sources=[mem_file])
        func = getattr(module, func_name + '_check_mem_torch')
        ret_func = (func, so_path)
        return ret_func
