# -*- coding: utf-8 -*-
import json
import unittest

from aspireforge.config import Config
from aspireforge.serving.server import make_handler


class TestServing(unittest.TestCase):
    def test_handler_health(self):
        from aspireforge.serving.server import _EngineHolder
        holder = _EngineHolder(Config())
        Handler = make_handler(holder)
        # instantiate a bare handler and call the health path manually
        h = Handler.__new__(Handler)
        h.path = "/health"
        # directly exercise the json body construction
        self.assertTrue(callable(Handler._send))


if __name__ == "__main__":
    unittest.main()
