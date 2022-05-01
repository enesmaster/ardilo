from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('docs/', views.docs, name="docs"),
    path('configrations/', views.configrations, name="config"),
    path('open/', views.open_the_door, name="open_the_door"),
    #USERS
    path('login/', views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    #WORKSHOPS
    path('workshop/<str:secret_key>', views.workshop, name='workshop'),
    path('control/', views.control_panel, name='control_panel'),
    
]
