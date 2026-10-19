# -*- coding: utf-8 -*-
"""Optional integrations with popular frameworks. Each module degrades gracefully
to the mock backend when the external dependency is not installed."""
from . import langchain, llamaindex, openai

__all__ = ["langchain", "llamaindex", "openai"]
