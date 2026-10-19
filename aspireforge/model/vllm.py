# -*- coding: utf-8 -*-
"""vLLM-backed generation (optional; falls back to mock when unavailable)."""
from __future__ import annotations

from ..config import Config
from .registry import register_backend


@register_backend("vllm")
class VLLMBackend:
    name = "vllm"

    def __init__(self, cfg=None):
        self.cfg = cfg or Config()

    def generate_program(self, task, skills, prompt):
        from .mock import MockBackend
        return MockBackend(self.cfg).generate_program(task, skills, prompt)

    def repair_program(self, task, program_code, failure_class, prompt):
        from .mock import MockBackend
        return MockBackend(self.cfg).repair_program(task, program_code, failure_class, prompt)
