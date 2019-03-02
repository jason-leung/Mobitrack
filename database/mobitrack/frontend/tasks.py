# Create your tasks here
from mobitrack.celery import app

@app.task
def addAndrea(x, y):
    print("andrea - add")
    return x + y
