# 配方：多智能体协作

1. 每个机器人一个 `AspireEngine` 实例 + 独立 `SkillLibrary`。
2. 共享只读的「中央技能库」（检索时合并多库）。
3. 失败案例集中复盘，根因分类结果跨机器人复用。
4. 用 `observability.MetricAccumulator` 汇总成功率/命中率。
