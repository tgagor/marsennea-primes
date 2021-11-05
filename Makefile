.PHONY: requirements clean

VENV_DIR = .venv

all: run

run: requirements
	( \
	   . $(VENV_DIR)/bin/activate; \
	   python lmarsennea.py; \
	)

.venv:
	python -m venv $(VENV_DIR)

create-venv: .venv

requirements: create-venv
	@( \
	   . $(VENV_DIR)/bin/activate; \
	   pip install -r requirements.txt; \
	)

clean:
	rm -f cache.dbm*
	rm -rf $(VENV_DIR)
