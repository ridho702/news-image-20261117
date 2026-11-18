#!/usr/bin/env python3
"""make.fun news-image-20261117 entry.

Copies the infographic built by build_image.py (entry.png, beside this
file) to the grader's output directory as /output/entry.png.
Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
out_dir.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "entry.png", out_dir / "entry.png")
print("wrote", out_dir / "entry.png")
