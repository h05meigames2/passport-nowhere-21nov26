#!/usr/bin/env python3
"""Copy the pre-rendered passport spread to $MAKEFUN_OUTPUT_DIR/entry.png.

The image is rendered at build time by gen_image.py and shipped as
entry.png in this repo. This program is STDLIB ONLY (os/shutil/sys) so it
runs in the grader's vanilla python:3.13 image with no extra packages.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(HERE, "out")


def main():
    if not os.path.isfile(SRC):
        print("missing entry.png next to main.py", file=sys.stderr)
        return 1
    os.makedirs(OUT_DIR, exist_ok=True)
    dst = os.path.join(OUT_DIR, "entry.png")
    shutil.copyfile(SRC, dst)
    print("saved", dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
