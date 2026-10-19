# 配方：评估指标

```python
from aspireforge.eval.metrics import success_rate, memory_hit_rate
from aspireforge.engine import AspireEngine

engine = AspireEngine(Config())
results = [engine.solve(make_task("e-%d" % i, engine.primitive_set)) for i in range(32)]
print(success_rate(results), memory_hit_rate(results))
```
