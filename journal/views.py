from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserCreationForm


def home(request):
    """Home page - shows different content for authenticated vs anonymous users"""
    return render(request, 'journal/home.html')


def register_view(request):
    """User registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('journal:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'journal/register.html', {'form': form})


@login_required
def dashboard(request):
    """User dashboard - requires login"""
    return render(request, 'journal/dashboard.html')


@login_required
def profile_view(request):
    """User profile view with basic information"""
    return render(request, 'journal/profile.html')


@login_required
def change_password_view(request):
    """Change user password"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('journal:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'journal/change_password.html', {'form': form})
