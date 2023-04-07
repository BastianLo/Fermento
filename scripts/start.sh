#!/bin/sh
pip freeze > requirements.txt
cd Fermento
cd Fermento
django-admin makemessages -a
cd ..
cd templates
django-admin makemessages -a
cd ..
cd recipe_manager
django-admin makemessages -a
cd ..
django-admin compilemessages
python3 manage.py runserver