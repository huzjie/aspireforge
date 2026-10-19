# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

"""Launch the stdlib HTTP server (visit http://127.0.0.1:8765/health)."""
from aspireforge.config import Config
from aspireforge.serving.server import serve

serve(Config(), host="127.0.0.1", port=8765)
