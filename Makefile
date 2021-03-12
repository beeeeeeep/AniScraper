.PHONY: dev devd build restart clean

dev:
	python3 copy_config.py
	sudo docker-compose -f $(dc-yml) up

devd:
	python3 copy_config.py
	sudo docker-compose -f $(dc-yml) up -d

build:
	python3 copy_config.py
	sudo docker-compose -f $(dc-yml) build

restart:
	sudo docker-compose -f $(dc-yml) restart

clean:
	sudo docker-compose -f $(dc-yml) down
