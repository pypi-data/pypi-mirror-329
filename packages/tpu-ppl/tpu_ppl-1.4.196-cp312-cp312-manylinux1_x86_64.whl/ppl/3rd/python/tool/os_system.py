import logging
import argparse
import subprocess
import os
import time
import shlex
import signal
from subprocess import Popen, PIPE

def _os_subprocess(cmd: list, time_out: int = 0):
    cmd_str = ""
    for s in cmd:
        cmd_str += str(s) + " "
    print("[Running]: {}".format(cmd_str))
    process = Popen(shlex.split(cmd_str), stdout=PIPE)
    st = time.time()
    while True:
        output = process.stdout.readline().rstrip().decode('utf-8')
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())

        if time_out > 0 and time.time() - st > time_out:
            os.kill(process.pid, signal.SIGTERM)
            print("[!Warning:TimeOut]: {}".format(cmd_str))
            return 2

    rc = process.poll()
    if rc == 0:
        print("[Success]: {}".format(cmd_str))
    else:
        print("[!Error]: {}".format(cmd_str))
        rc = 1
    return rc

def _os_system(cmd: list, time_out: int = 0):
    cmd_str = ""
    for s in cmd:
        cmd_str += str(s) + " "
    print("[Running]: {}".format(cmd_str))
    ret = os.system(cmd_str)
    if ret == 0:
        print("[Success]: {}".format(cmd_str))
    else:
        print("[!Error]: {}".format(cmd_str))
        return 1
    return 0
