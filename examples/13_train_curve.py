# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aspireforge.config import Config
from aspireforge.train_bench.train import train_skill

curve = train_skill(Config(), lr=0.15, steps=16)
print("skill %.4f -> %.4f (monotonic=%s)"
      % (curve.initial, curve.final, curve.monotonic()))
