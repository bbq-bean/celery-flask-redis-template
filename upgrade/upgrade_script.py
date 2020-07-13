import logging
import time


def verify_target(celery_task, user_vars):
    verify_logger = logging.getLogger('urban-garbanzo')

    # useful to reference task from inside task, yo.
    verify_logger.info('starting job with task id ' + str(celery_task.request.id))

    # log, update task
    verify_logger.info('working.. 0% complete..')
    celery_task.update_state(state='STARTED', meta={'current': '0%',
                                                    'status': "Starting.."})

    # pretend it takes time to finish
    for i in range(20, 101, 20):
        verify_logger.info('working.. {0}% complete..'.format(str(i)))
        celery_task.update_state(state='PROGRESS', meta={'current': str(i) + '%',
                                                         'status': "cOmPutiNg.."})
        time.sleep(10)

    # the actual work
    word_result = user_vars['pet 1'] + user_vars['pet 2']

    verify_logger.info('complete, returning result')
    celery_task.update_state(state='SUCCESS', meta={'current': '100%',
                                                    'status': "Success!"})

    return word_result


def configure_target(celery_task, user_vars):
    configure_logger = logging.getLogger('urban-garbanzo')

    # useful to reference task from inside task, yo.
    configure_logger.info('starting job with task id ' + str(celery_task.request.id))

    # log, update task
    configure_logger.info('working.. 0% complete..')
    celery_task.update_state(state='STARTED', meta={'current': '0%',
                                                    'status': "Starting.."})

    # pretend it takes time to finish
    for i in range(20, 101, 20):
        configure_logger.info('working.. {0}% complete..'.format(str(i)))
        celery_task.update_state(state='PROGRESS', meta={'current': str(i) + '%',
                                                         'status': "cOmPutiNg.."})
        time.sleep(10)

    # the actual work
    word_result = user_vars['pet 1'] + user_vars['pet 2']

    configure_logger.info('complete, returning result')
    celery_task.update_state(state='SUCCESS', meta={'current': '100%',
                                                    'status': "Success!"})

    return word_result
