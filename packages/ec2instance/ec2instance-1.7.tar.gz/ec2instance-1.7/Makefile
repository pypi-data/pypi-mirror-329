.PHONY: clean clean-build clean-pyc clean-test coverage dist docs help lint lint/flake8
.DEFAULT_GOAL := help

clean:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

test:
	uv run flake8 ec2instance tests
	uv run black --check ec2instance tests
	uv run update_readme_usage --check
	uv run pytest

coverage:
	uv run coverage run --source ec2instance -m pytest
	uv run coverage report -m
	uv run coverage html
	$(BROWSER) htmlcov/index.html

docs: ## Generate Sphinx HTML documentation, including API docs
	rm -f docs/ec2instance.rst
	rm -f docs/modules.rst
	uvx --from sphinx sphinx-apidoc -o docs/ ec2instance
	uvx --from sphinx $(MAKE) -C docs clean
	uvx --from sphinx $(MAKE) -C docs html
	xdg-open docs/_build/html/index.html

servedocs: docs ## Autoreload docs
	uvx --with sphinx --from watchdog watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: clean ## Build and release to PyPI
	uv build
	ls -l dist
	uv publish --token "$(pcregrep -o1 'password: (pypi-.+)$' ~/.pypirc)"


