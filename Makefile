init:  build run
	docker-compose exec api flask db upgrade
	docker-compose exec api flask admin init
	@echo "Init done, containers running"

build:
	docker-compose build

run:
	docker-compose up -d

db-migrate:
ifeq ($(message), undefined)
	docker-compose exec api flask db migrate
else
	docker-compose exec api flask db migrate -m "$(message)"
endif

db-upgrade:
	docker-compose exec api flask db upgrade

test-api:
	docker-compose exec api pytest -x -s tests

test-stock:
	docker-compose exec stock pytest -x -s tests
