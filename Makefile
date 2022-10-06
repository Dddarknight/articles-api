lint:
	poetry run flake8

install:
	poetry install

test-coverage:
	poetry run pytest --cov=api_server --cov-report xml

test:
	poetry run pytest