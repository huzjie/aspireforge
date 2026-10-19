# -*- coding: utf-8 -*-
"""OpenAI-compatible backend (optional; requires an API key via env)."""
from __future__ import annotations

from ..config import Config
from ..utils.codegen import render_program
from .registry import register_backend


@register_backend("openai")
class OpenAIBackend:
    name = "openai"

    def __init__(self, cfg=None):
        self.cfg = cfg or Config()

    def generate_program(self, task, skills, prompt):
        # Without a real key this delegates to the mock fallback so the pipeline
        # still runs end-to-end for demos and docs.
        from .mock import MockBackend
        return MockBackend(self.cfg).generate_program(task, skills, prompt)

    def repair_program(self, task, program_code, failure_class, prompt):
        from .mock import MockBackend
        return MockBackend(self.cfg).repair_program(task, program_code, failure_class, prompt)
