from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.wearingsession, name='index' ),
    url(r'^(?P<patientID>[\w.@+-]+)/$', views.wearingsession, name='wearingsession' ),
    path('pairmobitrack', views.pairmobitrack, name='pairmobitrack' ),
    path('pairmobitrack/submit/', views.formSubmit, name='formSubmit' ),
    path('pairmobitrack/stopMonitoring/', views.stopMonitoring, name='stopmonitor'),
    url(r'^pairmobitrack/(?P<task_id>[\w.@+-]+)/$', views.get_progress, name='task_status'),
]