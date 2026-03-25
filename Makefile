# Default Python (will be overridden on Windows)
PYTHON = python3

# Detect OS
ifeq ($(OS),Windows_NT)
	PYTHON = python
	SET_PYTHONPATH = set PYTHONPATH=src&&
else
	SET_PYTHONPATH = PYTHONPATH=src
endif

.PHONY: run install benchmark viz-demo

# Run the project
run:
	$(SET_PYTHONPATH) $(PYTHON) -m main

# Single-puzzle comparison: N runs per solver + figures/
benchmark:
	$(SET_PYTHONPATH) $(PYTHON) -m benchmark

# Interpretation + plots from synthetic expData (no full dataset run)
viz-demo:
	$(SET_PYTHONPATH) $(PYTHON) -m data_visualization --demo

# Install dependencies
install:
	$(PYTHON) -m pip install -r requirements.txt
