from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from pathlib import Path


from celery.result import AsyncResult
from frontend.tasks import *
from time import sleep

from rest_framework import generics

import json

MAC_ADDRESS = 'F7:83:98:15:21:07'

def get_progress(request, task_id):
    result = AsyncResult(task_id)
    response_data = {
        'state': result.state,
        'details': result.info,
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')

def index(request):
    print("INDEX")
    return render(request, 'frontend/index.html')

def wearingsession(request):
    return render(request, 'frontend/wearingsession.html')
 
def pairmobitrack(request):
    return render(request, 'frontend/pairmobitrack.html')

@csrf_exempt
def getStatus(request):
    if (request.method == 'POST'):
        print("Getting Status")
        path_MAC = MAC_ADDRESS.replace(":", "-")
        lock_folder = os.path.join(Path(os.path.dirname( __file__ )).parents[2], "lock")
        lock_file = os.path.join(lock_folder, path_MAC + "_lock.txt")

        if os.path.isfile(lock_file):
            currently_running = True
            print("file exists")
            with open(lock_file, 'r') as f:
                task_id = f.read()
        else:
            currently_running = False
            print("file doesnt exist")
            task_id = ""

    return HttpResponse(json.dumps({'task_id': task_id, 'currently_running': currently_running}), content_type='application/json')

@csrf_exempt
def stopMonitoring(request):
    if (request.method == 'POST'):
        x = stopTracking.delay(MAC_ADDRESS)
    return HttpResponse(json.dumps({'task_id':x.task_id}), content_type='application/json')

@csrf_exempt 
def formSubmit(request):
    print(request)
    if (request.method == 'POST'):
        data = json.loads(request.body)
        # For physical device
        #x = startTracking.delay(MAC_ADDRESS, data['wearLocation'], data['patientID'], data['led_on'], data['targetAngle'])

        # For mocking device
        x = startTrackingMock.delay(MAC_ADDRESS, data['wearLocation'], data['patientID'], data['led_on'], data['targetAngle'])


    return HttpResponse(json.dumps({'task_id':x.task_id}), content_type='application/json')
