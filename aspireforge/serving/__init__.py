# -*- coding: utf-8 -*-
"""Serving: stdlib HTTP server + command-line interface."""
from .server import make_handler, serve

__all__ = ["make_handler", "serve"]


def main(argv=None):
    from .cli import main as _main
    return _main(argv)
