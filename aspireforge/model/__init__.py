# -*- coding: utf-8 -*-
"""Model backends that turn prompts into control programs.

The ``mock`` backend is a fully deterministic, trainable stand-in: its ``skill``
scalar drives how faithfully it reproduces a task's required primitive sequence.
It shares the oracle with the simulator so a trained agent (skill=1.0) always
succeeds and a random one (skill=0.5) hits the random baseline.
"""
from .registry import register_backend, get_backend, list_backends
from . import mock, openai_backend, vllm, transformers_backend, anthropic

__all__ = ["register_backend", "get_backend", "list_backends"]
