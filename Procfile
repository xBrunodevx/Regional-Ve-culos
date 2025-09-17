release: python manage.py migrate
web: gunicorn regional_veiculos.wsgi:application --bind 0.0.0.0:$PORT
