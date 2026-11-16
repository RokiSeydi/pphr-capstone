# PPHR capstone - revision project for CHME0031
#
#   make setup          create the virtualenv and install everything
#   make drill WEEK=3   run one week's drills
#   make drills         run every week
#   make progress       show how far through you are
#   make verify         check the drills' tests against the reference solutions
#   make mock N=1       start a timed mock paper
#   make data           regenerate the synthetic capstone dataset
#   make lab            open JupyterLab

PY := .venv/bin/python
PYTEST := .venv/bin/pytest
WEEK ?=
N ?= 1

.PHONY: setup drill drills progress verify mock data lab clean help

help:
	@sed -n '2,10p' Makefile | sed 's/^# //; s/^#//'

setup:
	python3 -m venv .venv
	$(PY) -m pip install --upgrade pip --quiet
	$(PY) -m pip install -r requirements.txt
	$(PY) -m pip install -e .
	@echo "Ready. Try: make drill WEEK=1"

# Zero-pads WEEK so `make drill WEEK=3` finds test_week03.py.
drill:
	@test -n "$(WEEK)" || (echo "Which week? e.g. make drill WEEK=3"; exit 1)
	$(PYTEST) tests/test_week$(shell printf '%02d' $(WEEK)).py -v

drills:
	$(PYTEST)

progress:
	$(PY) scripts/progress.py

# Runs the identical tests against solutions/. Everything should pass; if it
# doesn't, the test is wrong rather than your answer.
verify:
	PPHR_TARGET=solutions $(PYTEST)

mock:
	$(PY) scripts/mock_exam.py $(N)

data:
	$(PY) scripts/make_capstone_data.py

lab:
	@echo "Starting JupyterLab. If a browser tab doesn't open to a page"
	@echo "that looks like Jupyter, copy the http://localhost:8888/... URL"
	@echo "printed below (with its ?token=...) into your browser by hand -"
	@echo "auto-launching a browser is unreliable on some Linux/WSL setups."
	@echo ""
	.venv/bin/jupyter lab --no-browser

clean:
	rm -rf .pytest_cache
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
