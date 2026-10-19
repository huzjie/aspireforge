# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aspireforge.config import Config
from aspireforge.train_bench.bench import run_zero_shot, run_repair_effect

print("zero_shot:", run_zero_shot(Config()))
print("repair   :", run_repair_effect(Config()))
