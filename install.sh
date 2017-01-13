#!/usr/bin/env bash

docker-compose up --build

docker exec $(basename `pwd`)_django_1 python manage.py migrate
docker exec $(basename `pwd`)_django_1 python manage.py createsuperuser