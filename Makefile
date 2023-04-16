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
	flake8 source/library
	flake8 source/service
	flake8 tests

unittests:
	coverage run -m pytest --durations=0 tests
	coverage html

# doctests:
# 	python -m doctest source/library/api.py
# 	python -m doctest source/library/app.py

tests: linting unittests
