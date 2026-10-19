# 训练说明

mock 后端是**可训练**的确定性模型：`skill` 标量从 0.5 单调升到 1.0，对应「生成保真度」
从随机基线升到完美。

```python
engine = AspireEngine(Config())
s0 = engine.train(["t%d" % i for i in range(16)], lr=0.15)  # skill 0.5 -> ~0.92
```

- `train_step` 用 `skill += lr * (1 - skill)`，几何收敛、**永不回退**（只升不降）。
- 生成保真度由 `boost=(skill-0.5)*2` 驱动：skill=0.5 → boost=0（纯随机），skill=1.0 → boost=1（恒正确）。
- 这是 clmforge/msaforge 反复验证的「单调趋 1」铁律：**别用对+1/错-1 的训练信号**，会被噪声压回 0。
