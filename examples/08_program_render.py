# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

"""Inspect the rendered control program source."""
from aspireforge.utils.codegen import render_program

prog = render_program("demo", ["move_to", "grasp", "place"])
print(prog.code)
print("primitives:", prog.primitives)
