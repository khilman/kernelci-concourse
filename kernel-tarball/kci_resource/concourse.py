#!/usr/bin/env python3

import sys
import kci_resource


def check():
    kci_resource.TarballResource(sys.stdin.read()).cmd_check()


def input():
    kci_resource.TarballResource(sys.stdin.read()).cmd_in(sys.argv[1])


def output():
    kci_resource.TarballResource(sys.stdin.read()).cmd_out(sys.argv[1])


if __name__ == "__main__":
    cmd = sys.argv[1]
    print(cmd)
    if cmd == "check":
        check()
    elif cmd == "in":
        input()
    elif cmd == "out":
        output()
