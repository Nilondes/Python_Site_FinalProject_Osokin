#!/bin/bash
cd clothing_rental
python3 manage.py migrate
python3 manage.py test
python3 manage.py runserver 0.0.0.0:8000