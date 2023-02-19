release: python manage.py makemigrations && python manage.py migrate
web: gunicorn onlyevents-drf-api.wsgi