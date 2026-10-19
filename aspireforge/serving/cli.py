# -*- coding: utf-8 -*-
"""Command-line interface."""
from __future__ import annotations

import argparse
import json

from ..config import Config, load_config
from ..engine import AspireEngine
from ..train_bench import summarize


def _cmd_doctor(cfg):
    from ..model import list_backends
    from ..robot.task import make_task
    engine = AspireEngine(cfg)
    lines = []
    lines.append("backends: %s" % ", ".join(list_backends()))
    lines.append("primitive_set: %s" % ", ".join(engine.primitive_set))
    # solve a single task end-to-end
    t = make_task("doctor-0", engine.primitive_set, cfg.robot.horizon)
    res = engine.solve(t)
    lines.append("solve(doctor-0): success=%s attempts=%d primitives=%s"
                 % (res.success, res.attempts, ", ".join(t.required_primitives)))
    # train a couple steps and re-solve
    engine.train(["doctor-1"], lr=0.5)
    lines.append("skill after train: %.4f" % engine.agent.backend.skill)
    return "\n".join(lines)


def _cmd_bench(cfg):
    return summarize(cfg)


def _cmd_solve(cfg, task_id):
    engine = AspireEngine(cfg)
    task = engine._task(task_id)
    res = engine.solve(task)
    print(json.dumps(res.to_dict(), indent=2, ensure_ascii=False))


def main(argv=None):
    parser = argparse.ArgumentParser(prog="aspireforge", description="Robot skill library + self-improving coding agent")
    parser.add_argument("--config", default=None, help="path to config.yaml")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("doctor", help="smoke-test the full pipeline")
    sub.add_parser("bench", help="run the benchmark suite")
    sp = sub.add_parser("solve", help="solve a single task")
    sp.add_argument("task_id", default="demo-0", nargs="?")

    args = parser.parse_args(argv)
    cfg = load_config(args.config) if args.config else Config()
    if args.cmd == "doctor":
        print(_cmd_doctor(cfg))
    elif args.cmd == "bench":
        print(_cmd_bench(cfg))
    elif args.cmd == "solve":
        _cmd_solve(cfg, args.task_id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
