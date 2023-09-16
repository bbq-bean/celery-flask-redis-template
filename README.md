# setup
dev

-clone, cd to upgrade

-duplicate tab, run these in different windows:

gunicorn --bind 0.0.0.0:5000 wsgi:app

celery worker -A upgrade.celery --loglevel=info



start redis-server in a third tab

can start and retrieve jobs for local testing

# setup with local docker
osx dev

-docker build, brew install redis

-start project like this in 3 tabs:

docker run -p 5000:5000 --env osx_dev="true" async_test:1 gunicorn --bind 0.0.0.0:5000 wsgi:app  
docker run --env osx_dev='true' async_test:1 celery worker -A upgrade.celery --loglevel=info  
redis-server

-post a job and get results:

curl -i -X POST http://127.0.0.1:5000/api/petcombiner/ -H 'Content-Type: application/json' -d '{"pet 1":"cat","pet 2":"dog"}  
curl http://127.0.0.1:5000/api/results/c6d363d9-3093-4684-9b88-6bb45d9ec8a3-or-whatever  
