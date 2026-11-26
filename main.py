#!/usr/bin/env python3
"""Deliver the 26 November 2026 front page to the grading sandbox.

compose.py has already painted entry.png from the pixel-art scene in
pixel.py; this entrypoint does the one job the grader needs and
nothing else: it puts that finished PNG at /output/entry.png. The
copy is byte for byte, it touches no network and it needs no clock,
so two runs of it always land the same file.

Run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
FINISHED = HERE / "entry.png"
PNG_MAGIC = bytes((0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A))


def deliver() -> Path:
    """Check the finished page is a real PNG, then copy it out."""
    data = FINISHED.read_bytes()
    if data[:8] != PNG_MAGIC:
        raise ValueError("entry.png is not a PNG file")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(FINISHED, target)
    return target


if __name__ == "__main__":
    deliver()
