PYTHON ?= python3

.PHONY: check sync-agents sync-user-skills check-user-skills

check:
	$(PYTHON) control/project.py check

sync-agents:
	$(PYTHON) control/project.py sync-agents

sync-user-skills:
	$(PYTHON) control/project.py sync-user-skills

check-user-skills:
	$(PYTHON) control/project.py check-user-skills
