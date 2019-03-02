# Create your tasks here
from celery.utils.log import get_task_logger
from celery import task

logger = get_task_logger(__name__)


@task
def startTracking(location, patientID):
    print("Async Offline: " + location + " ----- " + patientID)
    logger.info("Async Offline-Logger: " + location + " ----- " + patientID)

    # TODO: start monitoring here...


    return 27
