.PHONY: tests

docker_build:
	cp ~/.openai_template.env .
	docker compose -f docker-compose.yml build

docker_run: docker_build
	docker compose -f docker-compose.yml up

docker_run_gpu:
	docker run --name local-llm-bash-1 --gpus all -t nvidia/cuda

docker_rebuild:
	cp ~/.openai_template.env .
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

tests: linting unittests doctests

data: extract transform embed

extract:
	python source/service/cli.py extract

transform:
	python source/service/cli.py transform

embed:
	python source/service/cli.py embed
