from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def index(request):
    return render(request, 'frontend/index.html')

def wearingsession(request):
    return render(request, 'frontend/wearingsession.html')
    
def sessiondetail(request, sessionID):
	param = {}
	sessionID = request.GET.get('sessionID')
	param['sessionID'] = sessionID
	template = loader.get_template('frontend/sessiondetails.html')
	return HttpResponse(template.render(param, request))