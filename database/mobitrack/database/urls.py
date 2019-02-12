from django.urls import path

from . import views

urlpatterns = [
	path('database/latestsession/', views.LatestSessionListCreate.as_view() ),
    path('database/wearingsession/', views.WearingSessionListCreate.as_view() ),
    path('database/exerciseperiod/', views.ExercisePeriodListCreate.as_view() ),
]