BASEDIR=$(CURDIR)
DOCDIR=$(BASEDIR)/docs
DISTDIR=$(BASEDIR)/dist


pip-tools:
	pip install -U pip
	pip install -U poetry
	poetry add poetry-plugin-up --group dev
	poetry add pre-commit --group dev

requirements: pip-tools
	poetry install --with=dev,test

test:
	poetry run python manage.py test

run-infra:
	docker compose -f deploy/docker_compose_infra.yml up --build

run-compose:
	docker compose -f deploy/docker_compose.yml up --build

build:
	docker compose -f deploy/docker_compose.yml build

run:
	poetry run python manage.py compress --force && poetry run python manage.py runserver

import:
	poetry run python manage.py import_news

clean:
	docker compose -f deploy/docker_compose_infra.yml stop
	docker compose -f deploy/docker_compose_infra.yml rm pydigest_postgres
	docker volume rm pythondigest_pydigest_postgres_data
	docker volume rm pythondigest_pydigest_postgres_data_backups

restore:
	docker cp /home/axsapronov/Cloud/Dropbox/Backups/pydigest/postgresql-pythondigest-`date "+%Y-%m-%d"`.sqlc pydigest_postgres:/backups
	docker compose -f deploy/docker_compose_infra.yml exec postgres backups
	docker compose -f deploy/docker_compose_infra.yml exec postgres restore postgresql-pythondigest-`date "+%Y-%m-%d"`.sqlc

check:
	poetry run pre-commit run --show-diff-on-failure --color=always --all-files

update: pip-tools
	poetry update
	poetry run poetry up
	poetry run pre-commit autoupdate

migrate:
	poetry run python manage.py migrate
