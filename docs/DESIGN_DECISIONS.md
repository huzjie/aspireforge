# 设计决策记录

## 为什么成功信号共享单一 oracle

仿真与基准若各自实现「成功判定」，必然漂移（历史项目反复踩坑：基准用 `predicate`
字符串、预测用对象 id，恒 0 分）。统一 `oracle.program_correct(task_id, code)` 后，
skill=1.0 必然满分，skill=0.5 必然随机基线，曲线干净单调。

## 为什么 mock 用 `boost=(skill-0.5)*2`

早期 `score=skill*is_correct+noise` 在 skill=0.5 时已有 0.5 的恒定优势，recall 起点过高。
改成 `boost=(skill-0.5)*2`，skill=0.5 时 boost 恰为 0（纯随机），skill=1.0 时 boost=1（恒正确）。
这是 clmforge/chonkforge/msaforge 反复验证的铁律。

## 为什么技能库要内容寻址

技能 id = 代码的 md5，天然去重（相同代码不会重复入库）、天然可校验（id 与内容绑定）。
这是「分布式缓存免协商」的通用套路在技能库上的映射。

## 为什么修复置信度高于生成

生成是「从无到有」，修复是「缺什么补什么」。修复重加缺失原语用 `0.6+0.4*boost`，
比生成的 `0.5+0.5*boost` 高，保证复盘确实抬升成功率，而非走过场。
