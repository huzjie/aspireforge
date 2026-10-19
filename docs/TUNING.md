# 调优指南

| 参数 | 作用 | 建议 |
| --- | --- | --- |
| `reflect.max_repairs` | 失败后最多修复轮数 | 长程任务设 3~5，短程 1~2 |
| `skill.similarity_threshold` | 检索相似度门槛 | 过高漏召回，过低误命中；0.6 是稳妥起点 |
| `skill.max_skills` | 技能库容量 | 超限触发 LRU 淘汰，按任务规模设置 |
| `robot.primitive_set` | 原语集 | 与真实机器人能力对齐，别加未实现的伪原语 |
| `coder.model` | 后端 | 生产接 openai/vllm；离线用 mock |

## 经验

- 长程任务（required 原语 ≥ 5）冷启动成功率天然极低（0.5^5≈3%），**一定要开技能库**。
- 蒸馏门槛保持 `verified=True`，一次未验证的入库会污染后续所有检索。
