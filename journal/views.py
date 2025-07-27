from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
