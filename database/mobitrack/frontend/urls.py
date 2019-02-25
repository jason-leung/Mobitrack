from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index' ),
    path('wearingsession', views.wearingsession, name='wearingsession' ),
    path('pairmobitrack', views.pairmobitrack, name='pairmobitrack' ),
]