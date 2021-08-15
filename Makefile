SHELL := /bin/sh

runserver:
	docker exec -it dp-207_python_djangoserver_1 python ./django_app/manage.py runserver 0:5000

makemigrations:
	docker exec -it dp-207_python_djangoserver_1 python ./django_app/manage.py makemigrations

migrate:
	docker exec -it dp-207_python_djangoserver_1 python ./django_app/manage.py migrate

shell:
	docker exec -it dp-207_python_djangoserver_1 python ./django_app/manage.py shell

unittest_weather:
	docker exec -it dp-207_python_djangoserver_1 python ./django_app/manage.py test weather.tests

unittest_hotels:
	docker exec -it dp-207_python_djangoserver_1 python ./django_app/manage.py test hotels.tests

postgres:
	docker exec -it dp-207_python_postgres_server_1 sh && psql -U admin_pg postgres

start:
	cp ./django_app/.env.example ./django_app/.env && docker-compose up --build

build: start migrate