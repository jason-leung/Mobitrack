from django.shortcuts import render
from django.http import HttpResponse
from .models import WearingSession

def index(request):
	return HttpResponse("Displaying database index")
	
def dashboard(request, sessionID):
	wearingSession = get_object_or_404(WearingSession.objects, pk=sessionID)
	return HttpResponse("Displaying dashboard for session %s." % sessionID)
