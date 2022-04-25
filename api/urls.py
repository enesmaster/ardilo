from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('api/signal/', views.api_door_view, name="api_door_view"),
]
