#!/bin/sh
pip freeze > requirements.txt
#python3 manage.py makemessages -l en -l de -d djangojs
#django-admin compilemessages > /dev/null
python3 manage.py runserver