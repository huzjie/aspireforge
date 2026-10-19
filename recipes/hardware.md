# 配方：对接真实硬件

1. 原语集 `robot.primitive_set` 与真实 API 一一对应。
2. `Simulator.run` 换成真实执行 + 传感器回读。
3. 安全：生成的 Python 源码先静态校验 + 沙箱试跑。
4. `program_correct` 换成真实成功判定（位姿/夹爪传感器）。
