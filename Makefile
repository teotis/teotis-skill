PYTHON ?= python3

.PHONY: check sync-agents

check:
	$(PYTHON) control/project.py check

sync-agents:
	$(PYTHON) control/project.py sync-agents
