from django.db import models

# Initialize schema for WearingSession database
class WearingSession(models.Model):
	def __str__(self):
		return self.sessionID
		
	sessionID = models.CharField(max_length=16, primary_key=True)
	patientID = models.CharField(max_length=8)
	location = models.CharField(max_length=20)
	timeStamp = models.DateTimeField('date published')

# Initialize schema for ExercisePeriod database
class ExercisePeriod(models.Model):
	def __str__(self):
		return self.periodID
		
	periodID = models.CharField(max_length=8, primary_key=True)
	sessionID = models.ForeignKey(WearingSession, on_delete=models.PROTECT)
	duration = models.IntegerField()
	repetitions = models.IntegerField()
	timeStamp = models.DateTimeField('date published')