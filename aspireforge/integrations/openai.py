# -*- coding: utf-8 -*-
"""OpenAI-compatible completion hook (optional). Uses OPENAI_API_KEY if present,
otherwise falls back to the deterministic mock."""
from __future__ import annotations

import os

from ..config import Config


def chat_completion(prompt: str, cfg=None, **kwargs):
    """Best-effort completion. Real call needs OPENAI_API_KEY + requests; otherwise
    returns a deterministic mock completion so the pipeline never hard-fails."""
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        try:
            import requests
            r = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": "Bearer %s" % key},
                json={"model": kwargs.get("model", "gpt-4o-mini"),
                      "messages": [{"role": "user", "content": prompt}]},
                timeout=60,
            )
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        except Exception:
            pass
    return "def run(robot):\n    target = robot.goal()\n    robot.move_to(target)\n    return robot.success()\n"
