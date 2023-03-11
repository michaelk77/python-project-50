lint:
	poetry run flake8 app_scripts
test:
	poetry run pytest -vv
gendiff:
	poetry run gendiff
install:
	poetry install
publish:
	poetry publish --build
package-install:
	pip install --user dist/*.whl
coverage:
	poetry run pytest --cov=tests/ --cov-report xml