import os
import time


from flask import Flask
from flask import jsonify, request, url_for

from celery import Celery

from upgrade_script import verify_target
from upgrade_script import configure_target


app = Flask(__name__)
app.logger.info('flask initialized')

# export FLASK_ENV=development <- set this too
# if APP_ENVIRONMENT not set defaults to dev
APP_ENVIRONMENT = os.getenv('APP_ENVIRONMENT') or 'dev'

if APP_ENVIRONMENT == 'prod':
    # for later
    pass
elif APP_ENVIRONMENT == 'stag':
    # for later
    pass
else:
    # local dev
    app.logger.info('starting up local dev environment')
    
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'


# initialize celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
app.logger.info('celery initialized')

# ------------
# CELERY TASKS
# ------------
@celery.task(bind=True)
def verify_task(self, user_vars):
    # does the same thing but imported function from somewhere else
    result = verify_target(self, user_vars)

    return result


@celery.task(bind=True)
def upgrade_task(self, user_vars):
    # does the same thing but imported function from somewhere else
    result = configure_target(self, user_vars)

    return result


@celery.task
def task_results(task_id):
    '''
    :param task_id: task ID provided from celery when task is started
    :returns: celery.AsyncResult: Current information and status of running celery task
    '''
    return celery.AsyncResult(task_id)


# ------------
# FLASK ROUTES
# ------------
@app.route('/api/healthcheck/', methods=['GET'])
def healthcheck():
    return 'alive'


@app.route('/api/verify/', methods=['POST'])
def verify():
    user_vars = request.json

    task = verify_task.delay(user_vars)

    return jsonify({}), 202, {'Location': url_for('results', task_id=task.id)}


@app.route('/api/upgrade/', methods=['POST'])
def upgrade():
    user_vars = request.json

    task = upgrade_task.delay(user_vars)

    return jsonify({}), 202, {'Location': url_for('results', task_id=task.id)}


@app.route('/api/results/<task_id>', methods=['GET'])
def results(task_id):
    task = task_results(task_id)
    response = {'state': task.state, 'status': task.info}

    return response


if __name__ == '__main__':
    app.run(debug=True)
