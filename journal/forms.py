from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import GratitudeEntry


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.'
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='Optional.'
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='Optional.'
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class GratitudeEntryForm(forms.ModelForm):
    """
    Form for creating and editing gratitude entries with enhanced validation
    """
    
    class Meta:
        model = GratitudeEntry
        fields = ['title', 'content', 'mood', 'tags', 'is_private']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Give your entry a meaningful title...',
                'maxlength': '200'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': ('What are you grateful for today? '
                                'Share your thoughts and feelings...'),
                'required': True
            }),
            'mood': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ('Optional: family, friends, health, work... '
                                '(separate with commas)'),
                'maxlength': '200'
            }),
            'is_private': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make title field optional
        self.fields['title'].required = False
        self.fields['title'].help_text = (
            'Give your entry a meaningful title (optional)'
        )
        
        # Add empty option to mood field for HTML validation compliance
        mood_choices = [('', 'Select your mood...')] + \
            list(self.fields['mood'].choices)
        self.fields['mood'].choices = mood_choices
        
        # Add help text and validation to fields
        self.fields['content'].help_text = (
            'Express what you\'re grateful for in detail '
            '(minimum 10 characters)'
        )
        self.fields['tags'].help_text = 'Help categorize your entry (optional)'
        self.fields['is_private'].help_text = (
            'Uncheck to make this entry visible to others'
        )
        
        # Add Bootstrap validation classes
        for field_name, field in self.fields.items():
            if field_name != 'is_private':
                field.widget.attrs.update({
                    'class': (field.widget.attrs.get('class', '') +
                              ' form-control')
                })

    def clean_title(self):
        """Validate title field"""
        title = self.cleaned_data.get('title')
        if title:
            title = title.strip()
            if len(title) > 200:
                raise forms.ValidationError(
                    'Title must be 200 characters or less.'
                )
            if len(title) < 3:
                raise forms.ValidationError(
                    'Title must be at least 3 characters long.'
                )
        return title

    def clean_content(self):
        """Validate content field"""
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError('Content is required.')
        
        content = content.strip()
        if len(content) < 10:
            raise forms.ValidationError(
                'Please write at least 10 characters about what you\'re '
                'grateful for.'
            )
        if len(content) > 5000:
            raise forms.ValidationError(
                'Content must be 5000 characters or less.'
            )
        
        # Check for meaningful content (not just repeated characters)
        if len(set(content.replace(' ', '').lower())) < 3:
            raise forms.ValidationError(
                'Please write meaningful content about your gratitude.'
            )
        
        return content

    def clean_tags(self):
        """Validate and clean tags field"""
        tags = self.cleaned_data.get('tags')
        if tags:
            tags = tags.strip()
            # Split tags and validate
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            
            # Validate individual tags
            for tag in tag_list:
                if len(tag) > 30:
                    raise forms.ValidationError(
                        f'Tag "{tag}" is too long. Tags must be 30 '
                        f'characters or less.'
                    )
                if not tag.replace(' ', '').isalnum():
                    raise forms.ValidationError(
                        f'Tag "{tag}" contains invalid characters. Use only '
                        f'letters, numbers, and spaces.'
                    )
            
            # Limit number of tags
            if len(tag_list) > 10:
                raise forms.ValidationError(
                    'You can have a maximum of 10 tags per entry.'
                )
            
            # Return cleaned tags as comma-separated string
            return ', '.join(tag_list)
        return tags

    def clean(self):
        """Overall form validation"""
        cleaned_data = super().clean()
        
        # Additional validation can be added here for cross-field validation
        content = cleaned_data.get('content')
        title = cleaned_data.get('title')
        
        # If title and content are very similar, suggest improvement
        if title and content and title.lower() in content.lower()[:50]:
            self.add_error(
                'title',
                'Consider making your title more unique from your content.'
            )
        
        return cleaned_data
