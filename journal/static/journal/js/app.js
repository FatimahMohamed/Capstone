// Gratitude Journal Enhanced UX JavaScript

document.addEventListener('DOMContentLoaded', function() {
    
    // Keyboard Shortcuts
    document.addEventListener('keydown', function(e) {
        // Only trigger shortcuts if not in input fields
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
            return;
        }
        
        // Ctrl/Cmd + N: New Entry
        if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
            e.preventDefault();
            const newEntryBtn = document.querySelector('a[href*="create"]');
            if (newEntryBtn) {
                window.location.href = newEntryBtn.href;
            }
        }
        
        // Ctrl/Cmd + L: Entry List
        if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
            e.preventDefault();
            const entryListBtn = document.querySelector('a[href*="entries"]');
            if (entryListBtn) {
                window.location.href = entryListBtn.href;
            }
        }
        
        // Ctrl/Cmd + D: Dashboard
        if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
            e.preventDefault();
            const dashboardBtn = document.querySelector('a[href*="dashboard"]');
            if (dashboardBtn) {
                window.location.href = dashboardBtn.href;
            }
        }
        
        // ESC: Close modals or go back
        if (e.key === 'Escape') {
            const modal = document.querySelector('.modal.show');
            if (modal) {
                const bsModal = bootstrap.Modal.getInstance(modal);
                if (bsModal) bsModal.hide();
            }
        }
    });
    
    // Auto-save functionality for forms
    let autoSaveTimer;
    const forms = document.querySelectorAll('form[method="post"]');
    
    forms.forEach(form => {
        const textareas = form.querySelectorAll('textarea');
        const inputs = form.querySelectorAll('input[type="text"]');
        
        [...textareas, ...inputs].forEach(field => {
            field.addEventListener('input', function() {
                clearTimeout(autoSaveTimer);
                
                // Show auto-save indicator
                showAutoSaveIndicator();
                
                autoSaveTimer = setTimeout(() => {
                    saveFormData(form);
                }, 2000); // Auto-save after 2 seconds of inactivity
            });
        });
    });
    
    // Entry statistics animation
    animateNumbers();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Search form enhancements
    enhanceSearchForm();
    
    // Entry cards hover effects
    addEntryCardEffects();
});

function showAutoSaveIndicator() {
    let indicator = document.getElementById('auto-save-indicator');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'auto-save-indicator';
        indicator.className = 'position-fixed top-0 end-0 m-3 alert alert-info alert-sm';
        indicator.style.zIndex = '9999';
        indicator.innerHTML = '<i class="fas fa-save"></i> Auto-saving...';
        document.body.appendChild(indicator);
    }
    
    indicator.style.display = 'block';
    
    setTimeout(() => {
        indicator.style.display = 'none';
    }, 1000);
}

function saveFormData(form) {
    const formData = new FormData(form);
    const data = {};
    
    formData.forEach((value, key) => {
        data[key] = value;
    });
    
    // Save to localStorage as draft
    const formId = form.id || 'gratitude-form';
    localStorage.setItem(`draft_${formId}`, JSON.stringify(data));
    
    console.log('Draft saved:', data);
}

function loadFormData(form) {
    const formId = form.id || 'gratitude-form';
    const savedData = localStorage.getItem(`draft_${formId}`);
    
    if (savedData) {
        const data = JSON.parse(savedData);
        
        Object.keys(data).forEach(key => {
            const field = form.querySelector(`[name="${key}"]`);
            if (field && field.value === '') {
                field.value = data[key];
            }
        });
    }
}

function clearFormData(form) {
    const formId = form.id || 'gratitude-form';
    localStorage.removeItem(`draft_${formId}`);
}

function animateNumbers() {
    const numberElements = document.querySelectorAll('[data-animate-number]');
    
    numberElements.forEach(element => {
        const finalNumber = parseInt(element.textContent);
        let currentNumber = 0;
        const increment = Math.ceil(finalNumber / 30);
        
        const timer = setInterval(() => {
            currentNumber += increment;
            if (currentNumber >= finalNumber) {
                currentNumber = finalNumber;
                clearInterval(timer);
            }
            element.textContent = currentNumber;
        }, 50);
    });
}

function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function enhanceSearchForm() {
    const searchForm = document.querySelector('.search-form form, form[method="get"]');
    if (!searchForm) return;
    
    const searchInput = searchForm.querySelector('input[name="search"]');
    if (searchInput) {
        // Add search suggestions
        let searchTimer;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimer);
            searchTimer = setTimeout(() => {
                // Could implement search suggestions here
                console.log('Search:', this.value);
            }, 300);
        });
        
        // Focus search on Ctrl+F
        document.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
                e.preventDefault();
                searchInput.focus();
            }
        });
    }
}

// Toggle advanced search
function toggleAdvancedSearch() {
    const advancedSearch = document.getElementById('advanced-search');
    const toggleBtn = document.querySelector('[onclick="toggleAdvancedSearch()"] i');
    
    if (advancedSearch) {
        if (advancedSearch.style.display === 'none' || !advancedSearch.style.display) {
            advancedSearch.style.display = 'block';
            advancedSearch.classList.add('show');
            if (toggleBtn) toggleBtn.className = 'fas fa-times';
        } else {
            advancedSearch.style.display = 'none';
            advancedSearch.classList.remove('show');
            if (toggleBtn) toggleBtn.className = 'fas fa-cog';
        }
    }
}

function addEntryCardEffects() {
    const entryCards = document.querySelectorAll('.entry-card');
    
    entryCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Theme toggle functionality
function toggleTheme() {
    const body = document.body;
    const currentTheme = body.getAttribute('data-theme');
    const themeButton = document.querySelector('.theme-toggle i');
    
    if (currentTheme === 'dark') {
        body.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
        themeButton.className = 'fas fa-moon';
    } else {
        body.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
        themeButton.className = 'fas fa-sun';
    }
}

// Load saved theme
function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    const themeButton = document.querySelector('.theme-toggle i');
    
    document.body.setAttribute('data-theme', savedTheme);
    
    if (themeButton) {
        themeButton.className = savedTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
}

// Initialize theme on page load
loadTheme();

// Export functions for use in templates
window.GratitudeJournal = {
    saveFormData,
    loadFormData,
    clearFormData,
    toggleTheme
};
