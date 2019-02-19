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

# Handling GET and POST request for all exerciseperiod
class ExercisePeriodListCreate(generics.ListCreateAPIView):
	queryset = ExercisePeriod.objects.filter(sessionID='1f858e82313c4ca9')
	serializer_class = ExercisePeriodSerializer