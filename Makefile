.PHONY: clean cov covo format testreqs

clean:
	rm -rf dist build src/cml2tf.egg-info .pdm-build
	rm -rf htmlcov .coverage
	rm -rf .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -not -path "./.venv/*" -depth -exec rm -rf {} \;

cov:
	PYTHONPATH=src coverage run -m pytest
	coverage report

covo: cov
	coverage html
	open htmlcov/index.html

format:
	ruff check --fix
	ruff format

testreqs:
	pdm export -f requirements --without-hashes >tests/requirements.txt

