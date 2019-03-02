# Create your tasks here
#from mobitrack.celery import app
from celery.utils.log import get_task_logger
from celery import task

logger = get_task_logger(__name__)


@task
def addAndrea(x, y):
    print("andrea - add")
    return x + y
