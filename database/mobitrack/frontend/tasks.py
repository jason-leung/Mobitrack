# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery.decorators import task, shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(name="sum_two_numbers")
def add(x, y):
    logger.info("andrea - add")
    return x + y
