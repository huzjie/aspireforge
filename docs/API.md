# API 参考

## AspireEngine

- `solve(task, use_library=True, allow_repair=True) -> SolveResult`
- `train(task_ids, lr=0.1) -> float`（训练 mock skill）
- `library_size() -> int`

## SkillLibrary

- `put(skill) -> skill_id`
- `get(skill_id) -> Skill`
- `retrieve(tags, task_id, top_k, threshold) -> [RetrievalResult]`

## 后端

`aspireforge.model.get_backend(name, cfg)`；可用 `list_backends()` 查看（mock/openai/vllm/transformers/anthropic）。
