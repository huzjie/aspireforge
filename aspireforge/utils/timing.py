# -*- coding: utf-8 -*-
"""Wall-clock timing helpers."""
from __future__ import annotations

import time


class Stopwatch:
    def __init__(self):
        self._t0 = time.perf_counter()

    def elapsed(self) -> float:
        return time.perf_counter() - self._t0
