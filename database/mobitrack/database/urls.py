from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
	path('database/latestsession/', views.LatestSessionListCreate.as_view() ),
    path('database/wearingsession/', views.WearingSessionListCreate.as_view() ),
    path('database/exerciseperiod/', views.ExercisePeriodListCreate.as_view() ),
	url(r'^database/wearingsession/(?P<sessionID>[0-9]+)$', views.SessionDetailListCreate.as_view()),
]