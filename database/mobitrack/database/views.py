from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
@api_view(['GET'])
class ExercisePeriodListCreate(request):
	queryset = ExercisePeriod.objects.all()
	serializer_class = ExercisePeriodSerializer 

