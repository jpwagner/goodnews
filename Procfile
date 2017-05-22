web: bin/start-pgbouncer-stunnel gunicorn -w $WEB_CONCURRENCY wsgi:application -b 0.0.0.0:$PORT
worker: python worker.py
scheduler: python scheduler.py