export LANG=C.UTF-8

gunicorn — bind=0.0.0.0 — timeout 600 Artists.wsgi & celery -A Artists worker -l INFO