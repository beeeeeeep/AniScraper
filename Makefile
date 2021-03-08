.PHONY: dev devd build restart clean

dev:
	python3 copy_config.py
	source config.env
	docker-compose up

devd:
	python3 copy_config.py
	source config.env
	docker-compose up -d

build:
	python3 copy_config.py
	source config.env
	docker-compose build

restart:
	docker-compose restart

clean:
	docker-compose down
