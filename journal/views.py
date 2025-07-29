from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from .forms import CustomUserCreationForm, GratitudeEntryForm
from .models import GratitudeEntry


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
    # Get user's entries for statistics
    user_entries = GratitudeEntry.objects.filter(user=request.user)
    total_entries = user_entries.count()
    recent_entries = user_entries.order_by('-created_at')[:3]
    
    # Calculate mood distribution
    mood_stats = {}
    for mood_value, mood_label in GratitudeEntry.MOOD_CHOICES:
        count = user_entries.filter(mood=mood_value).count()
        mood_stats[mood_value] = {'label': mood_label, 'count': count}
    
    context = {
        'total_entries': total_entries,
        'recent_entries': recent_entries,
        'mood_stats': mood_stats,
    }
    return render(request, 'journal/dashboard.html', context)


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


@login_required
def create_entry(request):
    """Create a new gratitude entry"""
    if request.method == 'POST':
        form = GratitudeEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, 'Your gratitude entry has been created!')
            return redirect('journal:entry_detail', entry_id=entry.id)
    else:
        form = GratitudeEntryForm()
    return render(request, 'journal/create_entry.html', {'form': form})


@login_required
def entry_list(request):
    """List all user's entries with pagination"""
    entries = GratitudeEntry.objects.filter(
        user=request.user
    ).order_by('-created_at')
    paginator = Paginator(entries, 10)  # Show 10 entries per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'journal/entry_list.html', {'page_obj': page_obj})


@login_required
def entry_detail(request, entry_id):
    """View a specific entry"""
    entry = get_object_or_404(GratitudeEntry, id=entry_id, user=request.user)
    return render(request, 'journal/entry_detail.html', {'entry': entry})


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry"""
    entry = get_object_or_404(GratitudeEntry, id=entry_id, user=request.user)
    
    if request.method == 'POST':
        form = GratitudeEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your entry has been updated!')
            return redirect('journal:entry_detail', entry_id=entry.id)
    else:
        form = GratitudeEntryForm(instance=entry)
    
    return render(request, 'journal/edit_entry.html', {
        'form': form,
        'entry': entry
    })


@login_required
def delete_entry(request, entry_id):
    """Delete an entry"""
    entry = get_object_or_404(GratitudeEntry, id=entry_id, user=request.user)
    
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Your entry has been deleted.')
        return redirect('journal:entry_list')
    
    return render(request, 'journal/delete_entry.html', {'entry': entry})
