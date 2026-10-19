# 贡献指南

1. 所有代码零依赖（标准库优先）。
2. 新增后端在 `model/` 用 `@register_backend("name")` 注册，并在 `model/__init__.py` 显式 import。
3. 确定性优先：随机一律走 `utils/stable.py`，禁止裸 `random` / `hash()`。
4. 成功判定必须复用 `oracle`，禁止在基准里另写一份。
5. 每个模块至少一个单测（`aspireforge/tests/`）。
6. 提交前跑 `python -m compileall -q aspireforge` + `python -m unittest discover -s aspireforge/tests -t .`。
