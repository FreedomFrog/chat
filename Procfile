web: bin/start-pgbouncer daphne django_channels.asgi:application --port $PORT --bind 0.0.0.0
chatworker: python manage.py runworker --settings=django_channels.settings -v2