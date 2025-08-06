from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class GratitudeEntry(models.Model):
    """Model for storing user gratitude journal entries"""

    # Mood choices for the entry
    MOOD_CHOICES = [
        ('excellent', '😄 Excellent'),
        ('good', '😊 Good'),
        ('okay', '😐 Okay'),
        ('difficult', '😔 Difficult'),
        ('challenging', '😰 Challenging'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='gratitude_entries'
    )
    title = models.CharField(
        max_length=200,
        blank=True,
        help_text='Give your entry a meaningful title (optional)'
    )
    content = models.TextField(help_text='What are you grateful for today?')
    mood = models.CharField(
        max_length=20, choices=MOOD_CHOICES, default='good'
    )
    tags = models.CharField(
        max_length=200,
        blank=True,
        help_text='Optional tags separated by commas (e.g., family, work, '
                  'health)'
    )
    is_private = models.BooleanField(
        default=True, help_text='Keep this entry private'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Gratitude Entry'
        verbose_name_plural = 'Gratitude Entries'

    def __str__(self):
        return (f"{self.user.username} - {self.title} "
                f"({self.created_at.strftime('%Y-%m-%d')})")

    def get_tags_list(self):
        """Return tags as a list"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
