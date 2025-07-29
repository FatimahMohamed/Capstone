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
    
    # Journal Entry URLs
    path('entries/', views.entry_list, name='entry_list'),
    path('entries/create/', views.create_entry, name='create_entry'),
    path('entries/<int:entry_id>/', views.entry_detail, name='entry_detail'),
    path('entries/<int:entry_id>/edit/', views.edit_entry, name='edit_entry'),
    path('entries/<int:entry_id>/delete/', views.delete_entry,
         name='delete_entry'),
]
