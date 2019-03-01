from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Initialize schema for WearingSession database
class WearingSession(models.Model):
	def __str__(self):
		return self.sessionID
		
	sessionID = models.CharField(max_length=16, primary_key=True)
	patientID = models.CharField(max_length=8)
	location = models.CharField(max_length=20)
	timeStamp = models.DateTimeField('date published')
	
	def get_absolute_url(self):
		return ('wearing_session_detail', (),
				{
					'slug': self.slug,
				})
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.sessionID)
		super(WearingSession, self).save(*args, **kwargs)
		
	class Meta:
		ordering = ['timeStamp']
		
		def __unicode__(self):
			return self.sessionID

# Initialize schema for ExercisePeriod database
class ExercisePeriod(models.Model):
	def __str__(self):
		return self.periodID
		
	periodID = models.CharField(max_length=8, primary_key=True)
	patientID = models.CharField(max_length=8, default='12345678')
	sessionID = models.ForeignKey(WearingSession, on_delete=models.PROTECT)
	duration = models.IntegerField()
	repetitions = models.IntegerField()
	timeStamp = models.DateTimeField('date published')
	
