.PHONY: build publish test clean install-dev

all: clean install-dev coverage build publish

clean:
	rm -rf dist/ build/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +

install-dev:
	uv pip install -e ".[test]"

coverage:
	pytest --cov=quantum_trade_utilities tests/ -v

build:
	python -m build

publish:
	python -m twine upload dist/*