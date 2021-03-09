.PHONY: dev devd build restart clean

dev:
	python3 copy_config.py
	sudo docker-compose up

devd:
	python3 copy_config.py
	sudo docker-compose up -d

build:
	python3 copy_config.py
	sudo docker-compose build

restart:
	sudo docker-compose restart

clean:
	sudo docker-compose down
