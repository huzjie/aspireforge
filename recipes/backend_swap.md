# 配方：切换后端

```python
from aspireforge.config import Config
cfg = Config()
cfg.coder.model = "openai"          # openai / vllm / transformers / anthropic / mock
engine = AspireEngine(cfg, backend_name=cfg.coder.model)
```

未配置密钥时，各后端优雅降级到 mock，管线不硬失败。
