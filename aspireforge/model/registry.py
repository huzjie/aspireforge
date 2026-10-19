# -*- coding: utf-8 -*-
"""Backend registry."""
from __future__ import annotations

from typing import Dict, List

_BACKENDS: Dict[str, type] = {}


def register_backend(name):
    def deco(cls):
        _BACKENDS[name] = cls
        return cls
    return deco


def get_backend(name, cfg=None):
    if name not in _BACKENDS:
        raise ValueError("unknown backend %r; available=%s" % (name, list(_BACKENDS)))
    cls = _BACKENDS[name]
    try:
        return cls(cfg)
    except TypeError:
        return cls()


def list_backends() -> List[str]:
    return sorted(_BACKENDS)
