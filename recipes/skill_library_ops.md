# 配方：技能库运维

1. 容量：`max_skills` 超限自动 LRU 淘汰（`MemorySkillLibrary.evict`）。
2. 检索：标签重叠优先，嵌入相似度做二次精排（`retrieve`）。
3. 溯源审计：`skill.provenance` 记录来源任务、尝试次数、验证结果。
4. 去重：相同代码同 id，天然幂等（内容寻址）。
