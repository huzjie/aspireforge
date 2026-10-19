# aspireforge - zero-dependency robot skill library + self-improving coding agent
FROM python:3.12-slim

WORKDIR /app

COPY aspireforge/ aspireforge/
COPY pyproject.toml README.md ./
COPY configs.example.yaml ./

RUN pip install --no-cache-dir -e . 2>/dev/null || true

ENV ASPIREFORGE_CONFIG=/app/configs.example.yaml

EXPOSE 8765

CMD ["python", "-m", "aspireforge.serving.server"]
