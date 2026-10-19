# 从原型迁移到真实机器人

1. **替换 `robot/sim.py`**：把确定性仿真换成真实物理引擎（MuJoCo/Isaac），保留
   `reset/run` 接口与 `Trajectory` 结构。
2. **替换 `oracle.program_correct`**：接真实任务成功判定（目标位姿/夹爪闭合传感器）。
3. **替换 mock 后端**：`coder.model` 指向真实 LLM，提示词模板（`coder/prompt.py`）已按
   「声明式原语调用」设计，模型输出可直接被仿真检查。
4. **保留**：技能库、失败复盘、蒸馏、检索——这些与物理引擎无关，是纯工程件。

## 接口契约

- `Simulator.run(task, program_code) -> Trajectory`
- `CodingAgent.generate_program(task, library) -> Program`
- `SkillDistiller.distill(task, program, trajectory) -> Skill`
