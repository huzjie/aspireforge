# 控制程序生成提示词

你是机器人控制编程专家。给定任务指令与可用原语，生成一个 `run(robot)` 函数，
按正确顺序调用 `robot.<primitive>(target)`，最后返回 `robot.success()`。

## 输入

- 任务指令：`{instruction}`
- 可用原语：`{primitives}`
- 技能库参考：`{skills_block}`

## 规则

1. 只用列出的原语，不臆造新原语。
2. 顺序必须满足前置条件（先 `move_to` 再 `grasp`，抓取前 `open` 等）。
3. 失败时优先补充缺失原语，而不是整体重写。
