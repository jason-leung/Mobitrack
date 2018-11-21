from django.db import models

class WearingSession(models.Model):
	def __str__(self):
		return self.sessionID
		
	sessionID = models.CharField(max_length=16, primary_key=True)
	patientID = models.CharField(max_length=8)
	location = models.CharField(max_length=20)
	timeStamp = models.DateTimeField('date published')
	
class ExercisePeriod(models.Model):
	def __str__(self):
		return self.periodID
		
	periodID = models.CharField(max_length=8, primary_key=True)
	sessionID = models.CharField(max_length=16)
	duration = models.CharField(max_length=255)
	repetitions = models.CharField(max_length=20)
	timeStamp = models.DateTimeField('date published')