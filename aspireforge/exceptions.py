# -*- coding: utf-8 -*-
"""Custom exceptions."""


class AspireForgeError(Exception):
    """Base error for aspireforge."""


class UnknownBackendError(AspireForgeError):
    """Raised when a backend name is not registered."""


class SkillNotFoundError(AspireForgeError):
    """Raised when a skill id is not in the library."""
