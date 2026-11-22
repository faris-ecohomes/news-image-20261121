#!/usr/bin/env python3
"""news-image-20261121: one image summing up Saturday 21 November 2026.

The poster was drawn once, during the build, and ships in this
repository as entry.png (1024x1024). This program only copies it to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png), so the
graded run needs nothing but the Python standard library: no Pillow,
no fonts, no network, no clock and no randomness. Two runs write
byte-identical output because they copy the same file.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    size = os.path.getsize(dst)
    if size != os.path.getsize(src):
        raise SystemExit("copy is incomplete: %d of %d bytes" % (size, os.path.getsize(src)))
    with open(dst, "rb") as f:
        head = f.read(33)
    if len(head) < 33 or head[1:4] != b"PNG":
        raise SystemExit("not a PNG file: %s" % dst)
    width = int.from_bytes(head[16:20], "big")
    height = int.from_bytes(head[20:24], "big")
    if (width, height) != (1024, 1024):
        raise SystemExit("unexpected size: %dx%d" % (width, height))
    print("wrote", dst, "%dx%d" % (width, height), size, "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
