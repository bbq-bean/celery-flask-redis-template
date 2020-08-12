import logging
import time


def combine_pets(celery_task, user_vars):
    pet_logger = logging.getLogger('pet logger')

    # useful to reference task from inside task, yo.
    pet_logger.info('starting job with task id ' + str(celery_task.request.id))

    # log, update task
    pet_logger.info('working.. 0% complete..')
    celery_task.update_state(state='STARTED', meta={'current': '0/5',
                                                    'status': "Starting.."})

    #pretend it takes time to finish
    for i in range(5):
        pet_logger.info('working.. {0}/5 complete..'.format(str(i)))
        celery_task.update_state(state='PROGRESS', meta={'current': str(i) + '/5',
                                                         'status': "cOmPutiNg.."})
        time.sleep(1)

    # the actual work, combine the pets
    word_result = user_vars['pet 1'] + user_vars['pet 2']

    pet_logger.info('complete, returning result')
    celery_task.update_state(state='SUCCESS', meta={'current': '5/5',
                                                    'status': "Finished!",
                                                    'result': word_result})



