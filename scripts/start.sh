#!/bin/sh
pip freeze > requirements.txt
cd Fermento
django-admin compilemessages
python3 manage.py runserver