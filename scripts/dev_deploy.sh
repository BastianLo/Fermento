cd Fermento
python3 manage.py makemessages -l en -l de
cd ..
django-admin compilemessages > /dev/null
docker build -t fermento:localdev . && docker compose up