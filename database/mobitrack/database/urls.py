from django.urls import path

from . import views

urlpatterns = [
    path('wearingsession/', views.WearingSessionListCreate.as_view() ),
    path('exerciseperiod/', views.ExercisePeriodListCreate.as_view() ),
]