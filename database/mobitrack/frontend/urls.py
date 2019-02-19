from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index' ),
    path('wearingsession', views.wearingsession, name='wearingsession' ),
    path('wearingsession/<sessionID>', views.sessiondetails, name='sessiondetails' ),
]