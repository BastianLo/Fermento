#!/bin/bash
create-superuser () {
    local username="$1"
    local email="$2"
    local password="$3"
    cat <<EOF | python Fermento/manage.py shell
from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="$username").exists():
    User.objects.create_superuser("$username", "$email", "$password")
else:
    print('User "{}" exists already, not created'.format("$username"))
EOF
}
service nginx start

create-superuser ${USERNAME} ${EMAIL} ${PASSWORD}
cd Fermento
gunicorn --bind :6734 Fermento.wsgi
#python3 Fermento/manage.py runserver 0.0.0.0:8000