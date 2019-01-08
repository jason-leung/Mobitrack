from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django_tables2 import RequestConfig
from .models import WearingSession, ExercisePeriod
from .tables import ExercisePeriodTable as PTable

def index(request):
	return HttpResponse("Displaying database index")

def sessionDetail(request, sessionID):
	# Query the wearing session database with matching sessionID
	session = WearingSession.objects.filter(sessionID=sessionID).get()

	# Query the exercise period database with matching sessionID
	pResult = ExercisePeriod.objects.filter(sessionID_id=sessionID).select_related('sessionID').all()
	periods = [ExercisePeriod.objects.filter(periodID=pID).get() for pID in pResult]

	# Put it in a tabular form 	
	table = PTable(periods)
	RequestConfig(request).configure(table)
	
	wearingSession = get_object_or_404(WearingSession.objects, pk=sessionID)
	return render(request, 'database/sessionDetail.html', {'session':session, 'periods':periods, 'table':table})

