# -*- coding: utf-8 -*-
"""Hugging Face transformers-backed generation (optional; mock fallback)."""
from __future__ import annotations

from ..config import Config
from .registry import register_backend


@register_backend("transformers")
class TransformersBackend:
    name = "transformers"

    def __init__(self, cfg=None):
        self.cfg = cfg or Config()

    def generate_program(self, task, skills, prompt):
        from .mock import MockBackend
        return MockBackend(self.cfg).generate_program(task, skills, prompt)

    def repair_program(self, task, program_code, failure_class, prompt):
        from .mock import MockBackend
        return MockBackend(self.cfg).repair_program(task, program_code, failure_class, prompt)
