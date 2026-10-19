# 基准说明

基准全部从确定性 mock + 仿真器实测，每次运行结果完全一致：

- **skill_effect**：长程任务成功率随 skill 单调上升（0.5→1.0）。
- **repair_effect**：复盘修复 vs 单次生成的差距。
- **zero_shot**：冷启动 vs 库预热，长程未见任务的零样本成功率。
- **library**：技能库检索命中率。

复现：`python -m aspireforge.serving.cli bench`。
