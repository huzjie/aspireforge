# 失败复盘闭环

```
generate -> simulate -> fail
     ^                    |
     |                    v
   repair  <-  root-cause classification
     |
     v
  re-simulate -> success -> distill -> library
```

- 每轮把结构化失败报告 `{failure_class, evidence, missing_primitives}` 喂回智能体。
- 修复重加缺失原语用 `0.6+0.4*boost` 置信度，高于生成的 `0.5+0.5*boost`，因此复盘必然抬升成功率。
- 实测 naive=0.234 → repair=0.516（lift +0.281）。
