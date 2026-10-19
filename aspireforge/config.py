# -*- coding: utf-8 -*-
"""Configuration for aspireforge.

YAML is read through the bundled minimal parser (utils.yamlish) so the package stays
zero-dependency even when PyYAML is absent. If PyYAML is available it is preferred.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional


def _load_yaml(text: str) -> Dict[str, Any]:
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text) or {}
    except Exception:
        from .utils.yamlish import parse
        return parse(text)


@dataclass
class SkillConfig:
    backend: str = "memory"            # memory | sqlite
    hash: str = "sha256"
    max_skills: int = 4096
    similarity_threshold: float = 0.6
    embed_dim: int = 32


@dataclass
class CoderConfig:
    model: str = "mock"
    temperature: float = 0.0
    max_program_steps: int = 64
    prompt_template: str = "default"


@dataclass
class ReflectConfig:
    max_repairs: int = 3
    failure_classes: List[str] = field(default_factory=lambda: [
        "collision", "timing_error", "grasp_failure",
        "goal_not_reached", "precondition_violation", "none",
    ])


@dataclass
class RobotConfig:
    n_tasks: int = 128
    horizon: int = 64
    seed: int = 42
    primitive_set: List[str] = field(default_factory=lambda: [
        "move_to", "grasp", "place", "push", "rotate", "open", "close", "wait",
    ])


@dataclass
class BenchConfig:
    n_seen: int = 32
    n_unseen: int = 32
    episodes: int = 8
    long_horizon_primitives: int = 5


@dataclass
class Config:
    skill: SkillConfig = field(default_factory=SkillConfig)
    coder: CoderConfig = field(default_factory=CoderConfig)
    reflect: ReflectConfig = field(default_factory=ReflectConfig)
    robot: RobotConfig = field(default_factory=RobotConfig)
    bench: BenchConfig = field(default_factory=BenchConfig)
    # declared scale (informational, not instantiated as real tensors)
    skill_library_size: int = 90
    covered_tasks: int = 150

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Config":
        cfg = cls()
        if not d:
            return cfg
        for section in ("skill", "coder", "reflect", "robot", "bench"):
            if section in d and isinstance(d[section], dict):
                sub = getattr(cfg, section)
                for k, v in d[section].items():
                    if hasattr(sub, k):
                        setattr(sub, k, v)
        for k in ("skill_library_size", "covered_tasks"):
            if k in d:
                setattr(cfg, k, d[k])
        return cfg

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def load_config(path: Optional[str] = None) -> Config:
    if path is None:
        here = Path(__file__).resolve().parent
        path = str(here / "configs" / "default.yaml")
    p = Path(path)
    if p.exists():
        data = _load_yaml(p.read_text(encoding="utf-8"))
        return Config.from_dict(data)
    return Config()


def default_config() -> Config:
    return Config()
