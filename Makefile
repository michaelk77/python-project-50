lint:
	poetry run flake8 gendiff
test:
	poetry run pytest -vv
gendiff:
	poetry run gendiff
install:
	poetry install
build:
	poetry build
publish:
	poetry publish --build --dry-run
package-install:
	pip install --user dist/*.whl
coverage:
	poetry run pytest --cov=tests/ --cov-report xml