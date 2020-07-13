# urban-garbanzo

dev

-clone, cd to upgrade

-duplicate tab, run these in different windows:

gunicorn --bind 0.0.0.0:5000 wsgi:app

celery worker -A upgrade.celery --loglevel=info



start redis-server in a third tab

can start and retrieve jobs for local testing
