from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect


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
def stopMonitoring(request):
    if (request.method == 'POST'):
        x = stopTracking.delay(MAC_ADDRESS)
    return HttpResponse(json.dumps({'id':x.task_id}), content_type='application/json')

@csrf_exempt 
def formSubmit(request):
    print(request)
    if (request.method == 'POST'):
        data = json.loads(request.body)
        x = startTracking.delay(MAC_ADDRESS, data['wearLocation'], data['patientID'])
    return HttpResponse(json.dumps({'id':x.task_id}), content_type='application/json')
