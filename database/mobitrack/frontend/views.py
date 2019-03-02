from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

# from mobitrack.tasks import addAndrea

from rest_framework import generics

import json

def index(request):
    print("INDEX")
    return render(request, 'frontend/index.html')

def wearingsession(request):
    return render(request, 'frontend/wearingsession.html')
 
def pairmobitrack(request):
    return render(request, 'frontend/pairmobitrack.html')

@csrf_exempt 
def formSubmit(request):
    print(request)
    if (request.method == 'POST'):
        data = json.loads(request.body)
        print(data)

        # addAndrea.delay(2, 34)




    return render(request, 'frontend/pairmobitrack.html')
    #return HttpResponseRedirect('/')
    #return render(request, 'frontend/index.html')
