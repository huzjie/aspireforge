# aspireforge (zero-dependency)

PY ?= python

.PHONY: test bench doctor examples

test:
	$(PY) -m unittest discover -s aspireforge/tests -t .

bench:
	$(PY) -m aspireforge.serving.cli bench

doctor:
	$(PY) -m aspireforge.serving.cli doctor

examples:
	$(PY) examples/01_basic_solve.py
