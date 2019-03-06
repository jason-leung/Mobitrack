# Create your tasks here
from celery.utils.log import get_task_logger
from celery import task
from time import sleep



logger = get_task_logger(__name__)

@task(bind=True)
def stopTracking(self, mac_address):
    sleep(7)
    return True

@task(bind=True)
def startTracking(self, location, patientID):
    print("Async Offline: " + location + " ----- " + patientID)
    logger.info("Async Offline-Logger: " + location + " ----- " + patientID)


    self.update_state(
        state='ANDREA',
        meta={
           'current': 5,
            'total': 27,
        }
    )
    # TODO: start monitoring here...
    sleep(5)

    return 27
