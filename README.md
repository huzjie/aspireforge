# aspireforge

> 机器人「技能库 + 失败复盘自改进」编程智能体 —— 零依赖参考实现（NVIDIA ASPIRE 思路）

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Zero deps](https://img.shields.io/badge/dependencies-0-brightgreen)](pyproject.toml)

**一句话**：让一个编程智能体为机器人写控制程序，执行失败后从轨迹里**复盘根因、改码重试**，每次成功都**蒸馏成技能**存进可检索的技能库，让后续长程未见任务**零样本**直接命中。

这是一个从零实现、**零第三方依赖**、可直接运行的完整工程——不是 demo 玩具，填好配置就能跑通「生成 → 执行 → 复盘 → 修复 → 蒸馏 → 检索复用」全链路。

---

## 技术原理：为什么这样设计

机器人控制程序难在两点：① 长程任务要串对一长串原语，错一步全盘皆输；② 每次从零写，不沉淀经验。ASPIRE 的思路是把这两点都工程化：

1. **技能库（Skill Library）**——把「验证过有效」的控制代码片段结构化存储，按**标签 + 语义嵌入**检索。每个技能带完整 **provenance**（来源轨迹、尝试次数、验证结果），所以它不是「代码堆」，而是「经验记忆」。
2. **失败复盘（Failure Reflection）**——执行失败后捕获轨迹，**根因分类**（碰撞 / 时序 / 抓取失败 / 目标未达 / 前置条件未满足），把「缺哪个原语、为什么缺」写成结构化报告，喂回智能体改码。
3. **自改进闭环**——`生成 → 执行 → 复盘 → 修复 → 复测 → 蒸馏`，成功的方法回流进技能库，库越用越强。
4. **零样本泛化**——长程未见任务先查技能库，命中已验证的正确技能就直接成功，跳过生成。

---

## 四大工程件

| 组件 | 目录 | 核心职责 |
| --- | --- | --- |
| 技能库 | `skill/` | 内容寻址存储、标签索引、嵌入检索、LRU 淘汰、溯源 |
| 机器人世界 | `robot/` | 任务 / 观测 / 确定性仿真 / 轨迹；成功信号与基准**共享同一 oracle** |
| 编程智能体 | `coder/` | 提示词模板 + 检索增强的程序生成 |
| 失败复盘 | `reflect/` | 根因分类 → 修复 → 复测；成功蒸馏进技能库 |

**关键设计**：仿真与基准共用 `oracle.program_correct()`，mock 后端用 `boost=(skill-0.5)*2` 驱动生成保真度——skill=0.5 时 boost=0（随机基线 0.5^len），skill=1.0 时恒正确。这让每个数字可复现、随 skill 单调。

---

## 快速开始

```bash
# 冒烟自检（零依赖，Python 3.8+ 直接跑）
python -m aspireforge.serving.cli doctor

# 跑基准
python -m aspireforge.serving.cli bench

# 起 HTTP 服务
python -m aspireforge.serving.server
curl http://127.0.0.1:8765/health

# 单任务求解
python -m aspireforge.serving.cli solve demo-0
```

---

## 干货块：可复用的自改进闭环

```python
from aspireforge.config import Config
from aspireforge.reflect.loop import SelfRepairLoop
from aspireforge.robot.task import make_task
from aspireforge.skill import MemorySkillLibrary

cfg = Config()
loop = SelfRepairLoop(cfg, library=MemorySkillLibrary())
task = make_task("repair-demo", cfg.robot.primitive_set)

result = loop.run(task)          # 生成 -> 执行 -> 复盘 -> 修复 -> 复测
print(result.success, result.attempts, result.failure_history)
```

**复用要点**（踩过的坑，直接抄）：
- **失败报告要「结构化」而非「一句描述」**：`{failure_class, evidence, missing_primitives}` 三字段，修复器才拿得到可执行的「缺哪个原语」。
- **只蒸馏成功方法**：`provenance.verified=True` 是写入技能库的硬门槛，避免污染库。
- **mock 训练信号单调趋 1**：`boost=(skill-0.5)*2`，skill=0.5 时 boost 恰为 0（随机基线），训练里 skill 只升不降，曲线干净。
- **「已正确」判定走共享 oracle**：检索命中后仍要用 `program_correct()` 复核，别把未验证技能当命中。

---

## 基准（实测，可复现）

| 指标 | 结果 |
| --- | --- |
| skill 效果（长程成功率，0.5→1.0） | `0.154 → 1.000`（单调） |
| 复盘修复（naive → repair） | `0.234 → 0.516`（lift +0.281） |
| 零样本泛化（冷启动 → 库预热） | `0.156 → 1.000`（记忆命中） |
| 技能库检索命中率 | `1.000`（库 26 技能） |

> 长程未见任务的冷启动成功率 ≈ 0.5^5 ≈ 3%（随机基线），库预热后靠记忆命中拉到 ~100%。

---

## 项目结构

```
aspireforge/
├── skill/          # 技能库（内容寻址 + 检索 + 溯源）
├── robot/          # 任务 / 观测 / 仿真 / 轨迹
├── coder/          # 编程智能体（提示词 + 生成）
├── reflect/        # 失败复盘（根因分类 + 修复 + 闭环）
├── distill/        # 技能蒸馏
├── model/          # 后端（mock/openai/vllm/transformers/anthropic）
├── train_bench/    # 训练 + 基准
├── serving/        # HTTP 服务 + CLI
├── integrations/   # langchain / llamaindex / openai
├── utils/          # 确定性随机 / 哈希 / yamlish / codegen
└── configs/        # 默认配置
tests/ examples/ docs/ prompts/ recipes/ deploy/ Dockerfile k8s helm CI
```

## License

MIT
