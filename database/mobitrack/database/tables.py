import django_tables2 as tables
from .models import WearingSession, ExercisePeriod

# Create a wearingSessiond Table to display on details page
class WearingSessionTable(tables.Table):
    class Meta:
        model = WearingSession
        template_name = 'django_tables2/bootstrap.html'
        
# Create a exercisePeriod Table to display on details page
class ExercisePeriodTable(tables.Table):
    class Meta:
        model = ExercisePeriod
        template_name = 'django_tables2/bootstrap.html'