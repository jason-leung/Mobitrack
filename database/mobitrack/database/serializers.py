# Serializers define the API representation. It translates the data into JSON format
from rest_framework import serializers

from database.models import WearingSession, ExercisePeriod

class WearingSessionSerializer(serializers.ModelSerializer):    
    class Meta:
        model = WearingSession
        fields = '__all__'

class ExercisePeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExercisePeriod
        fields = '__all__'