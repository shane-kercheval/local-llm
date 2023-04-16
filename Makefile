.PHONY: tests

docker_build:
	docker compose -f docker-compose.yml build

docker_run: docker_build
	docker compose -f docker-compose.yml up

docker_rebuild:
	docker compose -f docker-compose.yml build --no-cache

docker_bash:
	docker compose -f docker-compose.yml up --build bash

docker_open: notebook mlflow_ui zsh

notebook:
	open 'http://127.0.0.1:8888/?token=d4484563805c48c9b55f75eb8b28b3797c6757ad4871776d'

zsh:
	docker exec -it local-llm-bash-1 /bin/zsh


linting:
	flake8 source/library
	flake8 source/service
	flake8 tests

unittests:
	coverage run -m pytest --durations=0 tests
	coverage html

doctests:
	python -m doctest source/library/api.py
	python -m doctest source/library/app.py

tests: linting unittests doctests
