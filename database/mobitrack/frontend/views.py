from django.shortcuts import render

def index(request):
    return render(request, 'frontend/index.html')

def wearingsession(request):
    return render(request, 'frontend/wearingsession.html')

def pairmobitrack(request):
    return render(request, 'frontend/pairmobitrack.html')