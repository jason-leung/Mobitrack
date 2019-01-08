import django_tables2 as tables
from .models import ExercisePeriod

# Create a exercisePeriod Table to display on details page
class ExercisePeriodTable(tables.Table):
    class Meta:
        model = ExercisePeriod
        template_name = 'django_tables2/bootstrap.html'