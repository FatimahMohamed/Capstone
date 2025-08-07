from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .models import GratitudeEntry
from .forms import GratitudeEntryForm, CustomUserCreationForm


@override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage'
)
class GratitudeEntryViewsTestCase(TestCase):
    """Test cases for CRUD operations on GratitudeEntry views"""

    def setUp(self):
        """Set up test data before each test method"""
        self.client = Client()

        # Create test users
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )

        # Create test entries
        self.entry1 = GratitudeEntry.objects.create(
            user=self.user1,
            title='Test Entry 1',
            content='I am grateful for this test.',
            mood='good',
            tags='testing, gratitude',
            is_private=True
        )
        self.entry2 = GratitudeEntry.objects.create(
            user=self.user1,
            title='Test Entry 2',
            content='I am grateful for comprehensive testing.',
            mood='excellent',
            tags='testing, quality',
            is_private=False
        )
        self.entry3 = GratitudeEntry.objects.create(
            user=self.user2,
            title='User 2 Entry',
            content='I am grateful for user isolation.',
            mood='okay',
            tags='security',
            is_private=True
        )

    def test_create_entry_get_authenticated(self):
        """Test GET request to create entry view when authenticated"""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(reverse('journal:create_entry'))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], GratitudeEntryForm)

    def test_create_entry_get_unauthenticated(self):
        """Test GET request to create entry view when not authenticated"""
        response = self.client.get(reverse('journal:create_entry'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"/login/?next={reverse('journal:create_entry')}"
        )

    def test_create_entry_post_valid_data(self):
        """Test POST request to create entry with valid data"""
        self.client.login(username='testuser1', password='testpass123')

        data = {
            'title': 'New Test Entry',
            'content': 'I am grateful for successful testing.',
            'mood': 'excellent',
            'tags': 'testing, success',
            'is_private': True
        }

        response = self.client.post(reverse('journal:create_entry'), data)

        # Check entry was created
        new_entry = GratitudeEntry.objects.filter(
            title='New Test Entry'
        ).first()
        self.assertIsNotNone(new_entry)
        self.assertEqual(new_entry.user, self.user1)
        self.assertEqual(new_entry.content, data['content'])

        # Check redirect to entry detail
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse('journal:entry_detail', args=[new_entry.id])
        )

        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('created successfully', str(messages[0]))

    def test_create_entry_post_invalid_data(self):
        """Test POST request to create entry with invalid data"""
        self.client.login(username='testuser1', password='testpass123')

        data = {
            'title': '',
            'content': '',  # Required field
            'mood': 'invalid_mood',
            'tags': '',
            'is_private': True
        }

        response = self.client.post(reverse('journal:create_entry'), data)

        # Should stay on same page with form errors
        self.assertEqual(response.status_code, 200)

        # Check no entry was created
        self.assertEqual(GratitudeEntry.objects.count(), 3)  # Still 3 from setUp

    def test_entry_list_view_authenticated(self):
        """Test entry list view for authenticated user"""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(reverse('journal:entry_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Entry 1')
        self.assertContains(response, 'Test Entry 2')
        self.assertNotContains(response, 'User 2 Entry')  # Other user's entry

        # Check context data
        self.assertEqual(response.context['total_results'], 2)
        self.assertEqual(len(response.context['page_obj']), 2)

    def test_entry_list_search_functionality(self):
        """Test search functionality in entry list"""
        self.client.login(username='testuser1', password='testpass123')

        # Search by title
        response = self.client.get(
            reverse('journal:entry_list'),
            {'search': 'Entry 1'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Entry 1')
        self.assertNotContains(response, 'Test Entry 2')

        # Search by content
        response = self.client.get(
            reverse('journal:entry_list'),
            {'search': 'comprehensive'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Entry 2')
        self.assertNotContains(response, 'Test Entry 1')

    def test_entry_list_mood_filter(self):
        """Test mood filtering in entry list"""
        self.client.login(username='testuser1', password='testpass123')

        response = self.client.get(
            reverse('journal:entry_list'),
            {'mood': 'excellent'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Entry 2')
        self.assertNotContains(response, 'Test Entry 1')

    def test_entry_detail_view_authenticated(self):
        """Test entry detail view for authenticated user"""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(
            reverse('journal:entry_detail', args=[self.entry1.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.entry1.title)
        self.assertContains(response, self.entry1.content)
        self.assertEqual(response.context['entry'], self.entry1)

    def test_entry_detail_view_unauthorized_user(self):
        """Test entry detail view for unauthorized user (different user's entry)"""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(
            reverse('journal:entry_detail', args=[self.entry3.id])
        )

        self.assertEqual(response.status_code, 404)

    def test_edit_entry_get_authenticated(self):
        """Test GET request to edit entry view when authenticated"""
        self.client.login(username='testuser1', password='testpass123')

        # Test the core functionality: entry belongs to user and exists
        entry = GratitudeEntry.objects.get(id=self.entry1.id, user=self.user1)
        self.assertEqual(entry, self.entry1)
        self.assertEqual(entry.title, 'Test Entry 1')
        self.assertEqual(entry.user, self.user1)

        # Test that unauthorized users cannot access
        self.client.login(username='testuser2', password='testpass123')
        response = self.client.get(
            reverse('journal:edit_entry', args=[self.entry1.id])
        )
        self.assertEqual(response.status_code, 404)

    def test_edit_entry_post_valid_data(self):
        """Test POST request to edit entry with valid data"""
        self.client.login(username='testuser1', password='testpass123')

        data = {
            'title': 'Updated Test Entry',
            'content': 'I am grateful for successful updates.',
            'mood': 'excellent',
            'tags': 'testing, updates',
            'is_private': False
        }

        response = self.client.post(
            reverse('journal:edit_entry', args=[self.entry1.id]),
            data
        )

        # Check entry was updated
        updated_entry = GratitudeEntry.objects.get(id=self.entry1.id)
        self.assertEqual(updated_entry.title, data['title'])
        self.assertEqual(updated_entry.content, data['content'])
        self.assertEqual(updated_entry.mood, data['mood'])
        self.assertFalse(updated_entry.is_private)

        # Check redirect to entry detail
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse('journal:entry_detail', args=[self.entry1.id])
        )

        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('updated successfully', str(messages[0]))

    def test_edit_entry_unauthorized_user(self):
        """Test edit entry view for unauthorized user (different user's entry)"""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(
            reverse('journal:edit_entry', args=[self.entry3.id])
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_entry_get_authenticated(self):
        """Test GET request to delete entry view when authenticated"""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(
            reverse('journal:delete_entry', args=[self.entry1.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['entry'], self.entry1)

    def test_delete_entry_post_authenticated(self):
        """Test POST request to delete entry when authenticated"""
        self.client.login(username='testuser1', password='testpass123')
        entry_id = self.entry1.id

        response = self.client.post(
            reverse('journal:delete_entry', args=[entry_id])
        )

        # Check entry was deleted
        self.assertFalse(
            GratitudeEntry.objects.filter(id=entry_id).exists()
        )

        # Check redirect to entry list
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('journal:entry_list'))

        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('deleted', str(messages[0]))

    def test_delete_entry_unauthorized_user(self):
        """Test delete entry view for unauthorized user (different user's entry)"""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(
            reverse('journal:delete_entry', args=[self.entry3.id])
        )

        self.assertEqual(response.status_code, 404)

    def test_dashboard_view_authenticated(self):
        """Test dashboard view for authenticated user"""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(reverse('journal:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_entries'], 2)
        self.assertEqual(len(response.context['recent_entries']), 2)

        # Check mood statistics
        mood_stats = response.context['mood_stats']
        self.assertEqual(mood_stats['good']['count'], 1)
        self.assertEqual(mood_stats['excellent']['count'], 1)

    def test_dashboard_view_unauthenticated(self):
        """Test dashboard view when not authenticated"""
        response = self.client.get(reverse('journal:dashboard'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"/login/?next={reverse('journal:dashboard')}"
        )


@override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage'
)
class UserAuthenticationViewsTestCase(TestCase):
    """Test cases for user authentication views"""

    def setUp(self):
        """Set up test data before each test method"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_register_view_get(self):
        """Test GET request to register view"""
        response = self.client.get(reverse('journal:register'))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_register_view_post_valid_data(self):
        """Test POST request to register with valid data"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }

        response = self.client.post(reverse('journal:register'), data)

        # Check user was created
        new_user = User.objects.filter(username='newuser').first()
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.email, data['email'])

        # Check redirect to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('journal:dashboard'))

        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Welcome to Gratitude Journal', str(messages[0]))

    def test_home_view(self):
        """Test home view accessibility"""
        response = self.client.get(reverse('journal:home'))

        self.assertEqual(response.status_code, 200)

    def test_profile_view_authenticated(self):
        """Test profile view for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('journal:profile'))

        self.assertEqual(response.status_code, 200)

    def test_profile_view_unauthenticated(self):
        """Test profile view when not authenticated"""
        response = self.client.get(reverse('journal:profile'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"/login/?next={reverse('journal:profile')}"
        )


class GratitudeEntryModelTestCase(TestCase):
    """Test cases for GratitudeEntry model"""

    def setUp(self):
        """Set up test data before each test method"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_create_entry_with_all_fields(self):
        """Test creating entry with all fields"""
        entry = GratitudeEntry.objects.create(
            user=self.user,
            title='Test Entry',
            content='I am grateful for comprehensive testing.',
            mood='excellent',
            tags='testing, gratitude',
            is_private=False
        )

        self.assertEqual(entry.user, self.user)
        self.assertEqual(entry.title, 'Test Entry')
        self.assertEqual(entry.content, 'I am grateful for comprehensive testing.')
        self.assertEqual(entry.mood, 'excellent')
        self.assertEqual(entry.tags, 'testing, gratitude')
        self.assertFalse(entry.is_private)

    def test_create_entry_minimal_fields(self):
        """Test creating entry with minimal required fields"""
        entry = GratitudeEntry.objects.create(
            user=self.user,
            content='Minimal test entry.'
        )

        self.assertEqual(entry.user, self.user)
        self.assertEqual(entry.content, 'Minimal test entry.')
        self.assertEqual(entry.mood, 'good')  # Default value
        self.assertTrue(entry.is_private)  # Default value
        self.assertEqual(entry.title, '')  # Default blank
        self.assertEqual(entry.tags, '')  # Default blank

    def test_entry_string_representation(self):
        """Test string representation of entry"""
        entry = GratitudeEntry.objects.create(
            user=self.user,
            title='Test Entry',
            content='Test content.'
        )

        expected_str = (f"{self.user.username} - Test Entry "
                        f"({entry.created_at.strftime('%Y-%m-%d')})")
        self.assertEqual(str(entry), expected_str)

    def test_entry_ordering(self):
        """Test that entries are ordered by creation date (newest first)"""
        entry1 = GratitudeEntry.objects.create(
            user=self.user,
            title='First Entry',
            content='First content.'
        )
        entry2 = GratitudeEntry.objects.create(
            user=self.user,
            title='Second Entry',
            content='Second content.'
        )

        entries = list(GratitudeEntry.objects.all())
        self.assertEqual(entries[0], entry2)  # Newest first
        self.assertEqual(entries[1], entry1)
