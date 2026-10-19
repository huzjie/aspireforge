# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

"""Zero-shot generalization: cold-start vs library-warmed on unseen tasks."""
from aspireforge.config import Config
from aspireforge.train_bench.bench import run_zero_shot

d = run_zero_shot(Config())
print("cold_zero_shot : %.3f (random baseline ~0.5**len)" % d["cold_zero_shot"])
print("warm_zero_shot : %.3f (memory-hit from library)" % d["warm_zero_shot"])
print("library_size   :", d["library_size"])
