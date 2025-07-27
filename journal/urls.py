from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'journal'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/change-password/', views.change_password_view, name='change_password'),
    path('login/', auth_views.LoginView.as_view(template_name='journal/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
