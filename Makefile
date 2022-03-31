.PHONY: dev devd build restart clean

dev:
	python3 copy_config.py
	sudo docker-compose up

run:
	python3 copy_config.py
	sudo docker-compose --profile novpn up -d

run-vpn:
	python3 copy_config.py
	sudo docker-compose --profile vpn up -d

build:
	python3 copy_config.py
	sudo docker-compose --profile novpn build

build-vpn:
	python3 copy_config.py
	sudo docker-compose --profile vpn build

restart:
	sudo docker-compose restart

clean:
	sudo docker-compose stop
	sudo docker-compose --profile vpn down --rmi all
	sudo docker-compose --profile novpn down --rmi all
