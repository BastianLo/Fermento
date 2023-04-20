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

# Collect static files and run migrations
python Fermento/manage.py collectstatic --noinput && python Fermento/manage.py migrate

create-superuser ${USERNAME} ${EMAIL} ${PASSWORD}
django-admin compilemessages > /dev/null 2>&1
echo 'Starting application'
echo "$(ls)"
gunicorn --bind :6734 --workers 3 --preload Fermento.wsgi