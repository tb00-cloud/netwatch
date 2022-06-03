#!/bin/bash

# LOCAL DEV
# ==========

dev-mysql:
	docker network create local_net0192 || true
	docker run --network local_net0192 -d --rm --name netwatch_mysql -v ~/python/netwatch/backend/sqlMigrations/:/data/application/ -p 3306:3306 -e MYSQL_ROOT_PASSWORD=qwerty mysql:latest --init-file /data/application/.init.sql

dev-mysql-stop:
	sudo docker kill netwatch_mysql || true

dev-backend:
#Wait for MySQL to be ready
	while ! mysqladmin ping -h localhost -P 3306 --protocol=tcp -u root -pqwerty --silent; do sleep 2; echo "Sleeping"; done
#Export ENV vars and run the app
	export MYSQL_HOST=localhost &&\
	export MYSQL_DB=myapp &&\
	export MYSQL_USER=root &&\
	export MYSQL_PASSWORD=qwerty &&\
	export ROOT_USER=root &&\
	export ROOT_PASSWORD=root &&\
	export CORE_LOG_LEVEL=info &&\
	exportHTTP_LOG_LEVEL=info &&\
	python3 -m backend . 

dev-client:
	gnome-terminal --tab --title="Client" -- yarn  --cwd client/ run serve

dev-nginx:
	gnome-terminal --tab --title="NGINX Proxy" -- docker run --network host --rm -it --name local-nginx -p 9090:909 -v ${PWD}/nginx-local-dev.conf:/etc/nginx/nginx.conf:rw nginx

dev-compose: dev-mysql-stop dev-mysql dev-nginx dev-client 
	gnome-terminal --tab --title="Backend" -- make dev-backend

# PRODUCTION
# ==========

build:
	yarn --cwd ./client/ run build 
	docker build . -t tb00/netwatch:beta

publish:
	docker push tb00/netwatch:beta

# PRODUCTION TESTING
# ==================
docker-up: dev-mysql-stop dev-mysql
	while ! mysqladmin ping -h localhost -P 3306 --protocol=tcp -u root -pqwerty --silent; do sleep 2; echo "Sleeping"; done
	gnome-terminal --tab --title="Docker Netwatch" -- docker run --network local_net0192 --rm -it -p 8080:8080 --name netwatch \
	-e MYSQL_HOST=netwatch_mysql \
	-e MYSQL_DB=myapp \
	-e MYSQL_USER=root \
	-e MYSQL_PASSWORD=qwerty \
	-e ROOT_USER=root \
	-e ROOT_PASSWORD=root \
	-e CORE_LOG_LEVEL=info \
	-e HTTP_LOG_LEVEL=info \
	netwatch:beta

docker-down: dev-mysql-stop
	sudo docker kill netwatch