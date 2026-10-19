# 快速开始

```bash
# 1) 冒烟自检
python -m aspireforge.serving.cli doctor

# 2) 跑基准
python -m aspireforge.serving.cli bench

# 3) 起 HTTP 服务
python -m aspireforge.serving.server
curl http://127.0.0.1:8765/health

# 4) 单任务求解
python -m aspireforge.serving.cli solve demo-0
```

零依赖，Python 3.8+ 可直接跑；不需要安装任何第三方包。
