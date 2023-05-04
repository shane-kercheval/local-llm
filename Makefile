.PHONY: tests

docker_build:
	docker compose -f docker-compose.yml build

docker_run: docker_build
	docker compose -f docker-compose.yml up

docker_rebuild:
	docker compose -f docker-compose.yml build --no-cache

docker_bash:
	docker compose -f docker-compose.yml up --build bash

api_docs:
	open http://localhost:8080/docs

streamlit:
	open http://localhost:8501/

zsh:
	docker exec -it local-llm-bash-1 /bin/zsh

linting:
	ruff check source/library
	ruff check source/service
	ruff check tests

unittests:
	coverage run -m pytest --durations=0 tests
	coverage html

doctests:
	python -m doctest source/library/scraping.py

tests: linting unittests

data: data_extract data_transform 

data_extract:
	python source/service/cli.py extract

data_transform:
	python source/service/cli.py transform

embed:
	python source/service/cli.py embed
