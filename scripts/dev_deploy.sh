#cd Fermento
#python3 manage.py makemessages -l en -l de -d djangojs
#cd ..
#django-admin compilemessages > /dev/null
pip freeze > requirements.txt
docker build -t fermento:localdev . && docker compose up