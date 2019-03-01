from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index' ),
    path('wearingsession', views.wearingsession, name='wearingsession' ),
    url(r'^wearingsession(?P<sessionID>[\w.@+-]+)/$', views.wearingsession, name='wearingsession' ),
    path('pairmobitrack', views.pairmobitrack, name='pairmobitrack' ),
    path('pairmobitrack/submit/', views.formSubmit, name='formSubmit' ),
]