#!/usr/bin/env python
"""
Management script for testing GratitudeEntry model functionality
This script demonstrates model operations and can be run via Django shell
"""

from django.contrib.auth.models import User
from journal.models import GratitudeEntry
from django.utils import timezone
from datetime import timedelta


def create_sample_entries():
    """Create sample gratitude entries for testing"""
    
    # Get or create admin user
    try:
        admin_user = User.objects.get(username='admin')
    except User.DoesNotExist:
        print("Admin user not found. Please create a superuser first.")
        return
    
    # Sample entries data
    sample_entries = [
        {
            'title': 'Morning Coffee',
            'content': 'I\'m grateful for my perfect cup of coffee this morning. It gave me the energy and warmth I needed to start my day positively.',
            'mood': 'good',
            'tags': 'morning, coffee, energy, routine'
        },
        {
            'title': 'Friend\'s Support',
            'content': 'My friend called me when I was feeling down and listened to me. I\'m so grateful to have such caring people in my life.',
            'mood': 'excellent',
            'tags': 'friendship, support, emotional, connection'
        },
        {
            'title': 'Sunny Weather',
            'content': 'The beautiful sunny weather today lifted my spirits. I spent time outdoors and felt refreshed and energized.',
            'mood': 'excellent',
            'tags': 'weather, nature, outdoors, mood'
        },
        {
            'title': 'Work Achievement',
            'content': 'I completed a challenging project at work today. I\'m grateful for the opportunity to learn and grow professionally.',
            'mood': 'good',
            'tags': 'work, achievement, growth, professional'
        }
    ]
    
    created_entries = []
    
    for i, entry_data in enumerate(sample_entries):
        # Create entry with different dates
        entry = GratitudeEntry.objects.create(
            user=admin_user,
            title=entry_data['title'],
            content=entry_data['content'],
            mood=entry_data['mood'],
            tags=entry_data['tags'],
            is_private=True
        )
        
        # Modify created_at to simulate entries from different days
        entry.created_at = timezone.now() - timedelta(days=i)
        entry.save()
        
        created_entries.append(entry)
    
    print(f"Created {len(created_entries)} sample entries")
    return created_entries


def display_entry_stats():
    """Display statistics about gratitude entries"""
    
    total_entries = GratitudeEntry.objects.count()
    print(f"Total gratitude entries: {total_entries}")
    
    if total_entries > 0:
        # Mood distribution
        print("\nMood Distribution:")
        for mood_value, mood_label in GratitudeEntry.MOOD_CHOICES:
            count = GratitudeEntry.objects.filter(mood=mood_value).count()
            print(f"  {mood_label}: {count}")
        
        # Recent entries
        recent_entries = GratitudeEntry.objects.order_by('-created_at')[:3]
        print(f"\nRecent Entries:")
        for entry in recent_entries:
            print(f"  • {entry.title} ({entry.created_at.strftime('%Y-%m-%d')})")


def cleanup_test_data():
    """Remove all test entries (use with caution)"""
    count = GratitudeEntry.objects.count()
    GratitudeEntry.objects.all().delete()
    print(f"Deleted {count} entries")


# Usage instructions for Django shell:
"""
To run this script in Django shell:

python manage.py shell

Then in the shell:
exec(open('test_model.py').read())

# Create sample data:
create_sample_entries()

# View statistics:
display_entry_stats()

# Clean up (optional):
# cleanup_test_data()
"""
