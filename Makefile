mysql-up:
	docker network remove local_net0192
	docker network create local_net0192
	docker run --network local_net0192 --rm -d --name netwatch_mysql -v ~/python/netwatch/backend/sqlMigrations/:/data/application/ -p 3306:3306 -e MYSQL_ROOT_PASSWORD=qwerty mysql:latest --init-file /data/application/.init.sql

mysql-down:
	sudo docker kill netwatch_mysql

local-backend-run:
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

build:
	yarn --cwd ./client/ run build 
	docker build . -t tb00/netwatch:beta

publish:
	docker push tb00/netwatch:beta

# FOR LOCAL TESTING (Docker and non-Docker)
dev-docker-up: mysql-up
	while ! mysqladmin ping -h localhost -P 3306 --protocol=tcp -u root -pqwerty --silent; do sleep 2; echo "Sleeping"; done
	docker run --network local_net0192 --rm -it -p 8080:8080 --name netwatch \
	-e MYSQL_HOST=netwatch_mysql \
	-e MYSQL_DB=myapp \
	-e MYSQL_USER=root \
	-e MYSQL_PASSWORD=qwerty \
	-e ROOT_USER=root \
	-e ROOT_PASSWORD=root \
	-e CORE_LOG_LEVEL=info \
	-e HTTP_LOG_LEVEL=info \
	netwatch:beta

dev-docker-down: mysql-down
	sudo docker kill netwatch

dev-up: mysql-up local-backend-run
#will not start client. Do this separately

dev-down: mysql-down