# -*- coding: utf-8 -*-
"""Zero-dependency HTTP server (stdlib http.server).

Endpoints:
  GET  /health               -> {"status": "ok"}
  GET  /v1/skills            -> list library skills
  POST /v1/solve             -> solve a task (JSON body: {"task_id": "..."})
  GET  /v1/models            -> list available backends
"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from ..config import Config
from ..engine import AspireEngine


class _EngineHolder:
    def __init__(self, cfg):
        self.cfg = cfg
        self.engine = AspireEngine(cfg)


def make_handler(holder):
    class Handler(BaseHTTPRequestHandler):
        def _send(self, code, obj):
            body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            path = urlparse(self.path).path
            if path == "/health":
                return self._send(200, {"status": "ok", "service": "aspireforge"})
            if path == "/v1/models":
                from ..model import list_backends
                return self._send(200, {"models": list_backends()})
            if path == "/v1/skills":
                skills = [s.to_dict() for s in holder.engine.library.all()]
                return self._send(200, {"skills": skills, "count": len(skills)})
            return self._send(404, {"error": "not found"})

        def do_POST(self):
            path = urlparse(self.path).path
            if path == "/v1/solve":
                length = int(self.headers.get("Content-Length", "0"))
                body = json.loads(self.rfile.read(length) or b"{}")
                tid = body.get("task_id", "demo-0")
                task = holder.engine._task(tid)
                res = holder.engine.solve(task)
                return self._send(200, res.to_dict())
            return self._send(404, {"error": "not found"})

        def log_message(self, *args):
            pass

    return Handler


def serve(cfg=None, host="127.0.0.1", port=8765):
    cfg = cfg or Config()
    holder = _EngineHolder(cfg)
    httpd = HTTPServer((host, port), make_handler(holder))
    print("aspireforge serving on http://%s:%d" % (host, port), flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == "__main__":
    serve()
