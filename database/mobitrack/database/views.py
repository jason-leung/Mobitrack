from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext

from rest_framework import generics

from .models import WearingSession, ExercisePeriod
from .serializers import WearingSessionSerializer, ExercisePeriodSerializer

# Handling GET and POST request for all wearingsession
class WearingSessionListCreate(generics.ListCreateAPIView):
	queryset = WearingSession.objects.all()
	serializer_class = WearingSessionSerializer

# Handling GET and POST request for all wearingsession
class LatestSessionListCreate(generics.ListCreateAPIView):
	queryset = WearingSession.objects.order_by('-timeStamp')[:5]
	serializer_class = WearingSessionSerializer

# Handling GET and POST request for exerciseperiod search
class ExercisePeriodListCreate(generics.ListCreateAPIView):
	queryset = ExercisePeriod.objects.all()
	serializer_class = ExercisePeriodSerializer

# Handling GET and POST request for all wearingsession
class SessionDetailListCreate(generics.ListCreateAPIView):
	def get_queryset(self):		
		queryset = ExercisePeriod.objects.all()
		sessionID = self.kwargs['query']
		print(sessionID)
		if sessionID:
			queryset = queryset.filter(sessionID=sessionID)
		
		return queryset
	serializer_class = ExercisePeriodSerializer
