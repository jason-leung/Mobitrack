from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # /database/sessionID
    path('<sessionID>/dashboard', views.dashboard, name='dashboard'),
]