.PHONY: server, migrate, upgrade, db, lint, commit

server:
	poetry run flask run --reload --debug

migrate:
	poetry run flask db migrate

upgrade:
	poetry run flask db upgrade

lint:
	poetry run pre-commit run --all-files

commit:
	poetry run cz commit

db:
	migrate upgrade
