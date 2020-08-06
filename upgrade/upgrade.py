from flask import Flask
from flask import jsonify, request, url_for

from celery import Celery

from pet_scripts import combine_pets


app = Flask(__name__)

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
def combine_pets(self, user_vars):
    # does the same thing but imported function from somewhere else
    result = combine_pets(self, user_vars)

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


@app.route('/api/petcombiner/', methods=['POST'])
def pet_combiner():
    user_vars = request.json

    task = combine_pets.delay(user_vars)

    return jsonify({}), 202, {'Location': url_for('results', task_id=task.id)}


@app.route('/api/results/<task_id>', methods=['GET'])
def results(task_id):
    task = task_results(task_id)
    response = {'state': task.state, 'status': task.info}

    return response


if __name__ == '__main__':
    app.run(debug=True)
