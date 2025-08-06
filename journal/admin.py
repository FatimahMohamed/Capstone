from django.contrib import admin
from .models import GratitudeEntry


@admin.register(GratitudeEntry)
class GratitudeEntryAdmin(admin.ModelAdmin):
    """Admin interface for GratitudeEntry model"""

    list_display = ['title', 'user', 'mood', 'created_at', 'is_private']
    list_filter = ['mood', 'is_private', 'created_at', 'user']
    search_fields = ['title', 'content', 'tags', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Entry Information', {
            'fields': ('user', 'title', 'content')
        }),
        ('Metadata', {
            'fields': ('mood', 'tags', 'is_private')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Optimize queries with select_related"""
        return super().get_queryset(request).select_related('user')
