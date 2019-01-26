from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    # Url for session detail page. example: /database/sessionID
    path('<sessionID>/', views.sessionDetail, name='detail'),
]