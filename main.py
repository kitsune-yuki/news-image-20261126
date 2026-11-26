#!/usr/bin/env python3
"""Ship the finished front page for the 26 November 2026 entry.

The front page is already composed (compose.py) from the pixel-art
scene (pixel.py) and the day's news; this entrypoint only copies the
finished PNG to the output directory. It needs no network, draws
nothing and writes identical bytes on every run.

Run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"


def ship():
    if not SOURCE.is_file():
        raise FileNotFoundError(f"missing finished front page: {SOURCE}")
    target = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, target / "entry.png")


if __name__ == "__main__":
    ship()
