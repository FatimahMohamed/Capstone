// Gratitude Journal Enhanced UX JavaScript
/*global document, window, bootstrap, localStorage, console, setTimeout, FormData, clearTimeout, setInterval, clearInterval, parseInt, Math, Object, JSON, Array */

(function () {
    'use strict';

    function showAutoSaveIndicator() {
        var indicator = document.getElementById('auto-save-indicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'auto-save-indicator';
            indicator.className = 'position-fixed top-0 end-0 m-3 alert alert-info alert-sm';
            indicator.style.zIndex = '9999';
            indicator.innerHTML = '<i class="fas fa-save"></i> Auto-saving...';
            document.body.appendChild(indicator);
        }

        indicator.style.display = 'block';

        setTimeout(function () {
            indicator.style.display = 'none';
        }, 1000);
    }

    function saveFormData(form) {
        var formData = new FormData(form),
            data = {},
            formId = form.id || 'gratitude-form';

        formData.forEach(function (value, key) {
            data[key] = value;
        });

        // Save to localStorage as draft
        localStorage.setItem('draft_' + formId, JSON.stringify(data));

        console.log('Draft saved:', data);
    }

    function loadFormData(form) {
        var formId = form.id || 'gratitude-form',
            savedData = localStorage.getItem('draft_' + formId),
            data;

        if (savedData) {
            data = JSON.parse(savedData);

            Object.keys(data).forEach(function (key) {
                var field = form.querySelector('[name="' + key + '"]');
                if (field && field.value === '') {
                    field.value = data[key];
                }
            });
        }
    }

    function clearFormData(form) {
        var formId = form.id || 'gratitude-form';
        localStorage.removeItem('draft_' + formId);
    }

    function animateNumbers() {
        var numberElements = document.querySelectorAll('[data-animate-number]');

        numberElements.forEach(function (element) {
            var finalNumber = parseInt(element.textContent, 10),
                currentNumber = 0,
                increment = Math.ceil(finalNumber / 30),
                timer;

            timer = setInterval(function () {
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
        var tooltipTriggerList = Array.prototype.slice.call(
            document.querySelectorAll('[data-bs-toggle="tooltip"]')
        );
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    function enhanceSearchForm() {
        var searchForm = document.querySelector(
                '.search-form form, form[method="get"]'
            ),
            searchInput,
            searchTimer;

        if (!searchForm) {
            return;
        }

        searchInput = searchForm.querySelector('input[name="search"]');
        if (searchInput) {
            // Add search suggestions
            searchInput.addEventListener('input', function () {
                clearTimeout(searchTimer);
                searchTimer = setTimeout(function () {
                    // Could implement search suggestions here
                    console.log('Search:', searchInput.value);
                }, 300);
            });

            // Focus search on Ctrl+F
            document.addEventListener('keydown', function (e) {
                if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
                    e.preventDefault();
                    searchInput.focus();
                }
            });
        }
    }

    function addEntryCardEffects() {
        var entryCards = document.querySelectorAll('.entry-card');

        entryCards.forEach(function (card) {
            card.addEventListener('mouseenter', function () {
                this.style.transform = 'translateY(-5px) scale(1.02)';
            });

            card.addEventListener('mouseleave', function () {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        var autoSaveTimer,
            forms;

        // Keyboard Shortcuts
        document.addEventListener('keydown', function (e) {
            var newEntryBtn,
                entryListBtn,
                dashboardBtn,
                modal,
                bsModal;

            // Only trigger shortcuts if not in input fields
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                return;
            }

            // Ctrl/Cmd + N: New Entry
            if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
                e.preventDefault();
                newEntryBtn = document.querySelector('a[href*="create"]');
                if (newEntryBtn) {
                    window.location.href = newEntryBtn.href;
                }
            }

            // Ctrl/Cmd + L: Entry List
            if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
                e.preventDefault();
                entryListBtn = document.querySelector('a[href*="entries"]');
                if (entryListBtn) {
                    window.location.href = entryListBtn.href;
                }
            }

            // Ctrl/Cmd + D: Dashboard
            if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
                e.preventDefault();
                dashboardBtn = document.querySelector('a[href*="dashboard"]');
                if (dashboardBtn) {
                    window.location.href = dashboardBtn.href;
                }
            }

            // ESC: Close modals or go back
            if (e.key === 'Escape') {
                modal = document.querySelector('.modal.show');
                if (modal) {
                    bsModal = bootstrap.Modal.getInstance(modal);
                    if (bsModal) {
                        bsModal.hide();
                    }
                }
            }
        });

        // Auto-save functionality for forms
        forms = document.querySelectorAll('form[method="post"]');

        forms.forEach(function (form) {
            var textareas = form.querySelectorAll('textarea'),
                inputs = form.querySelectorAll('input[type="text"]'),
                allFields = Array.prototype.slice.call(textareas).concat(
                    Array.prototype.slice.call(inputs)
                );

            allFields.forEach(function (field) {
                field.addEventListener('input', function () {
                    clearTimeout(autoSaveTimer);

                    // Show auto-save indicator
                    showAutoSaveIndicator();

                    autoSaveTimer = setTimeout(function () {
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

    // Export functions for use in templates
    window.GratitudeJournal = {
        saveFormData: saveFormData,
        loadFormData: loadFormData,
        clearFormData: clearFormData
    };

}());
