from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import GratitudeEntry


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class GratitudeEntryForm(forms.ModelForm):
    """Form for creating and editing gratitude entries"""
    
    class Meta:
        model = GratitudeEntry
        fields = ['title', 'content', 'mood', 'tags', 'is_private']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Give your entry a meaningful title...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'What are you grateful for today? Share your thoughts and feelings...'
            }),
            'mood': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional: family, friends, health, work... (separate with commas)'
            }),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add help text to fields
        self.fields['content'].help_text = 'Express what you\'re grateful for in detail'
        self.fields['tags'].help_text = 'Help categorize your entry (optional)'
        self.fields['is_private'].help_text = 'Uncheck to make this entry visible to others'
