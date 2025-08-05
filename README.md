# Gratitude Journal

![Screenshot of the 'my journal entries' page](readme/Screenshot%202025-08-05%20095511.png)

## Overview
Gratitude Journal is a Django-powered web application designed to help users cultivate a daily gratitude practice through digital journaling. The back-end of the application is python-based and the front-end incorporates HTML, CSS, Javascript and Bootstrap 5. 

The platform provides a personal, secure space for users to record and reflect on what they're grateful for each day. Users are able to create, view, edit and delete their gratitude entries.

The application aims to promote mental well-being and positive thinking by making gratitude journaling accessible, engaging, and sustainable. Users can track their emotional journey, build consistent writing habits, and gain insights into their gratitude patterns over time.

## Table of Contents

## UX Design

### User Stories

The user stories for the Gratitude Journal application have been carefully crafted to ensure the development process remains user-centered and focused on delivering real value to people seeking to build a meaningful gratitude practice. These stories serve as the foundation for feature development, testing criteria, and project prioritization.

Each user story follows the standard Agile format: "As a [type of user], I want [some goal] so that [some reason]." The user stories are organized using the MoSCoW method to guide development priorities.

#### Must Haves

**User Story 1: User Registration and Authentication**

As a new user, I want to create an account and log in securely so that I can have a personal, private space for my gratitude journal.  


**Acceptance Criteria:**
- User can register with username, email, and password
- Password must meet security requirements (minimum length, complexity)
- User receives confirmation message upon successful registration
- User is automatically logged in after registration
- User can log in with username and password
-  User can log out securely
- User sessions are managed securely
- Failed login attempts show appropriate error messages

**User Story 2: Create Gratitude Entries**

As a logged-in user, I want to write and save gratitude entries so that I can record what I'm grateful for each day.  


**Acceptance Criteria:**
- User can access entry creation form from dashboard
- User can write gratitude content (minimum 10 characters, maximum 5000)
- User can select mood from predefined options (Excellent, Good, Okay, Difficult, Challenging)
- User can optionally add a title (max 200 characters)
- User can optionally add tags separated by commas
- User can set entry privacy (private/shareable)
- Form validates required fields before submission
- Character count is displayed in real-time
- User receives confirmation message upon successful creation
- User is redirected to entry detail view after creation

**User Story 3: View and Manage Personal Entries**

As a logged-in user, I want to view, edit, and delete my gratitude entries so that I can manage my personal gratitude journal.  


**Acceptance Criteria:**
- User can view a list of all their entries
- Entries are displayed with title, date, mood, and content preview
- User can click on an entry to view full details
- User can edit existing entries
- User can delete entries with confirmation prompt
- Only the entry author can view/edit/delete their entries
- Entry timestamps show creation and last modified dates
- Entries are sorted by newest first by default

**User Story 4: Dashboard Overview**

As a logged-in user, I want to see an overview of my gratitude journey so that I can track my progress and be motivated to continue.  


**Acceptance Criteria:**
- Dashboard shows total number of journal entries
- Dashboard displays recent entries (last 3)
- Dashboard shows mood distribution statistics
- User can navigate to create new entry from dashboard
- User can navigate to view all entries from dashboard
- Dashboard displays personalized welcome message
- Quick action buttons are prominently displayed

**User Story 5: User Profile Management**

As a logged-in user, I want to view and manage my profile information so that I can maintain my account details.  


**Acceptance Criteria:**
- User can view their profile information (username, name, email, join date)
- User can change their password
- Password change requires current password verification
- User receives confirmation after successful password change
- Profile shows last login date
- User can navigate back to dashboard from profile

#### Should Haves

**User Story 6: Search and Filter Entries**

As a user with many journal entries, I want to search and filter my entries so that I can quickly find specific entries or content.  


**Acceptance Criteria:**
- User can search entries by title, content, or tags
- User can filter entries by mood
- User can filter entries by date range
- User can sort entries by date, title, or mood
- Search results show number of matching entries
- User can clear all filters to return to full list

**User Story 7: Entry Pagination**

As a user with many journal entries, I want to navigate through my entries in manageable chunks so that the page loads quickly and is easy to browse.  


**Acceptance Criteria:**
- Entry list shows 10 entries per page
- Pagination controls are clearly visible
- User can navigate to first, previous, next, and last pages
- Current page number is highlighted
- Page numbers are clickable
- Pagination works with search and filter results
- URL reflects current page for bookmarking

**User Story 8: Enhanced User Experience Features**

As a user, I want to have a smooth and intuitive experience so that I enjoy using the gratitude journal regularly.  


**Acceptance Criteria:**
- Responsive design works on desktop, tablet, and mobile
- Keyboard shortcut (Ctrl+D for dashboard)
- Form auto-save functionality for long entries
- Character count displays for text fields
- Smooth transitions and hover effects
- Consistent styling and branding throughout

**User Story 9: Mood Tracking and Visualisation**

As a user, I want to track my mood patterns over time so that I can understand my emotional journey.  


**Acceptance Criteria:**
- Dashboard shows mood distribution statistics
- Mood icons are visually distinct and colorful
- Mood counts are displayed with visual indicators
- Recent entries show mood with appropriate colors
- Mood filter in entry list shows all available moods
- Mood statistics exclude zero counts for cleaner display

#### Could Haves

**User Story 10: Gratitude Prompts and Inspiration**

As a user, I want to receive daily gratitude prompts so that I have inspiration when I'm unsure what to write about.  


**Acceptance Criteria:**
- Dashboard displays a daily gratitude prompt
- Prompts rotate and provide variety
- Prompts are thoughtful and engaging
- User can refresh to get a new prompt
- Prompts are stored in database for consistency
- Different prompts for different moods or themes

**User Story 11: Streak Tracking**

As a user, I want to track my writing streak so that I stay motivated to write regularly.  


**Acceptance Criteria:**
- Dashboard shows current writing streak (consecutive days)

**User Story 12: Entry Templates and Quick Entry**

As a busy user, I want to have quick ways to create entries so that I can maintain my gratitude practice even on busy days.  


**Acceptance Criteria:**
- Pre-defined templates for common gratitude themes
- Quick entry mode with minimal fields
- Voice-to-text capability for mobile users
- One-click entry creation from prompts
- Templates can be customized by user
- Quick entry still captures essential data (mood, content)

### Wireframes

The wireframes for the Gratitude Journal application were created using Balsamiq Wireframes to visualize the user interface design and layout before development. These wireframes helped establish the information architecture, user flow, and responsive design considerations for both desktop and mobile experiences.


![desktop and mobile wireframes for the my entries page](readme/My-entries-wireframes.png)







