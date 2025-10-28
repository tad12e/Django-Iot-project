from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('verify-email', views.Verify_email, name='Verify_email'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('recieving', views.recieve, name='recieve'),
    path('dashboard', views.dashboard, name='dashboard'),
]