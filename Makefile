.PHONY: clean format

clean:
	rm -rf dist build src/cml2tf.egg-info
	find . -type d -name __pycache__ -not -path "./.venv/*" -depth -exec rm -rf {} \;

format:
	ruff check --fix
	ruff format

