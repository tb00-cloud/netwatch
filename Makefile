sql_up:
	docker run --rm -d --name netwatch_mysql -v ~/python/netwatch/backend/sqlMigrations/:/data/application/ -p 3306:3306 -e MYSQL_ROOT_PASSWORD=qwerty mysql:latest --init-file /data/application/.init.sql

sql_down:
	sudo docker kill netwatch_mysql

run:
	while ! mysqladmin ping -h localhost -P 3306 --protocol=tcp -u root -pqwerty --silent; do sleep 2; echo "Sleeping"; done
	export MYSQL_HOST=localhost && export MYSQL_DB=myapp &&	export MYSQL_USER=root &&	export MYSQL_PASSWORD=qwerty &&	export ROOT_USER=root && export ROOT_PASSWORD=root && python3 -m backend . 

up: sql_up run
down: sql_down