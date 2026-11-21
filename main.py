#!/usr/bin/env python3
"""VELMORA — The Poster for a Place That Isn't There (make.fun entry).

The program writes one image to /output/entry.png: a travel poster for
Velmora, an island that floats above a sea of clouds and does not exist.
The image is pre-rendered by tools/render_poster.py (Pillow, build time
only) and shipped in assets/poster.png; this entry program only copies it,
so it runs in the sandbox with no network, no clock and no randomness, and
is byte-identical on every run.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "assets", "poster.png")
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copyfile(SRC, OUT)
print("wrote", OUT)
