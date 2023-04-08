#!/bin/sh
pip freeze > requirements.txt
cd Fermento
#python3 manage.py makemessages -l en -l de
#django-admin compilemessages > /dev/null
python3 manage.py runserver