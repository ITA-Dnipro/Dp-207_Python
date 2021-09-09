# e-mandruy django app
### Repository setup:
1. Clone this repository:
```
git clone https://github.com/ITA-Dnipro/Dp-207_Python_e-mandruy.git
```
2. Create .env files out of .env.example files for each folder with .env.example file, for example like this:
```
.
├──pgadmin4
    .env
    .env.example
    Dockerfile
    README.md
```
### How to use docker-compose:
1. Run command to build and start docker-compose
```
docker-compose -p mandruy_setup -f ${PWD}/docker-compose.yml up --build -d
```
2. Run command to start already created docker-compose
```
docker-compose -p mandruy_setup -f ${PWD}/docker-compose.yml -d start
```
3. Run command to stop docker-compose
```
docker-compose -p mandruy_setup -f ${PWD}/docker-compose.yml down
```
### Django commands:
1. Run django makemigrations command
```
docker exec -it mandruy_setup_django_server_1 /bin/sh -c "python django_app/manage.py makemigrations"
```
2. Run django migrate command
```
docker exec -it mandruy_setup_django_server_1 /bin/sh -c "python django_app/manage.py migrate"
```
3. Run django runserver command
```
docker exec -it mandruy_setup_django_server_1 /bin/sh -c "python django_app/manage.py runserver 0.0.0.0:5000"
```
