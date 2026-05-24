PYTHON ?= python3

.PHONY: check sync-agents

check:
	$(PYTHON) tools/project.py check

sync-agents:
	$(PYTHON) tools/project.py sync-agents
