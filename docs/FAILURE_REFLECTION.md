# 失败复盘设计

## 根因分类

失败轨迹进入 `FailureAnalyzer`，确定性映射到六类根因：

| 类别 | 触发 |
| --- | --- |
| `goal_not_reached` | 缺少 `move_to` |
| `grasp_failure` | 缺少 `grasp` |
| `timing_error` | 缺少 `wait` / 顺序错 |
| `precondition_violation` | 缺少 `open`/`close`/`rotate` |
| `collision` | 缺少 `push`/`place` |
| `none` | 无特定根因 |

## 修复闭环

每轮修复把失败报告（类别 + 证据 + 缺失原语）作为条件喂回编程智能体，重写程序并复测，最多 `reflect.max_repairs` 轮。修复的「重加缺失原语」置信度高于朴素生成（0.6+0.4·boost vs 0.5+0.5·boost），因此修复必然抬升成功率。

## 关键：为什么复盘能学到东西

只有**成功**的程序才被蒸馏进技能库，且带完整溯源（来源轨迹、尝试次数、验证结果）。这让技能库成为「经验记忆」，而不是「代码堆」——每个条目都经过执行验证。
