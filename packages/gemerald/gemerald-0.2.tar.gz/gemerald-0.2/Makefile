DEFAULT: install
.PHONY: all $(MAKECMDGOALS)

ci: example coverage lint
	black --check gemerald

example:
	export PYTHONPATH=$$PWD && cd example && rm -fr public && python -m gemerald .

format:
	black gemerald

lint:
	pylint --rcfile pyproject.toml gemerald

codedoc:
	rm -r docs/codedoc || true
	pdoc -o docs/codedoc ./gemerald !gemerald._test* !gemerald.strategies._test*

setup:
	deactivate || true
	rm -rf venv || true
	python -m venv venv
	. venv/bin/activate && python -m pip install -e '.[dev]'
	echo "Please activate virtual environment installed in 'venv' dir"

install:
	python -m pip install .

coverage:
	coverage run -m pytest
	coverage report -m
