.PHONY: requirements clean

VENV_DIR = .venv

.venv:
	python -m venv $(VENV_DIR)

create-venv: .venv

requirements: create-venv
	( \
	   source .venv/bin/activate; \
	   pip install -r requirements.txt; \
	)

clean:
	rm -f cache.dbm*
	rm -rf $(VENV_DIR)
