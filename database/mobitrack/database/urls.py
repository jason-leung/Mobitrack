from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
	path('database/latestsession/', views.LatestSessionListCreate.as_view() ),
    path('database/wearingsession/', views.WearingSessionListCreate.as_view() ),
    path('database/exerciseperiod/', views.ExercisePeriodListCreate.as_view() ),
	url(r'^database/exerciseperiod/(?P<sessionID>[\w.@+-]+)/$', views.SessionDetailListCreate.as_view()),
]