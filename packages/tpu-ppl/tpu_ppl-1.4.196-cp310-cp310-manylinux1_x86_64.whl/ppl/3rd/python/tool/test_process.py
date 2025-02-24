import os
import argparse
import numpy as np

def test_processor(test_func):
    def wrapper(*args, **kwargs):
        parser = argparse.ArgumentParser()
        parser.add_argument("--path", type=str, default="./", help="target npz file path")
        parser.add_argument("--dir", type=str, help="target main function")
        parser.add_argument("--tole", type=str, default = "0.99,0.99", help="cos euc")
        parser.add_argument("--chip", type=str, help="chip")

        cmd_args = parser.parse_args()

        dir = kwargs.get('dir') if 'dir' in kwargs else cmd_args.dir
        tole = kwargs.get('tole') if 'tole' in kwargs else cmd_args.tole
        inp_npz = cmd_args.path + f"test_{dir}/data/{dir}_input.npz"
        ori_npz = cmd_args.path + f"test_{dir}/data/{dir}_tar.npz"
        out_npz = "torch.npz"
        tpu_out = np.load(inp_npz)

        chip = kwargs.get('chip', cmd_args.chip)
        kwargs.update({'chip': chip})
        dic = test_func(tpu_out, **kwargs)

        np.savez(out_npz, **dic)

        cmd = ["npz_help.py", "compare", ori_npz, out_npz, "-vv --tolerance", tole]
        os.system(" ".join(cmd))

    return wrapper
