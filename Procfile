release: python manage.py makemigrations && python manage.py migrate
web: gunicorn onlyevents_drf_api.wsgi