// Service Worker for Gratitude Journal
// Caches critical resources to eliminate render blocking on repeat visits

const CACHE_NAME = 'gratitude-journal-v1';
const CRITICAL_RESOURCES = [
    '/',
    '/static/journal/css/style.css',
    '/static/journal/js/app.js',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
];

// Install event - cache critical resources
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Caching critical resources');
                return cache.addAll(CRITICAL_RESOURCES);
            })
            .catch(error => {
                console.log('Cache install failed:', error);
            })
    );
    self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// Fetch event - serve from cache first for critical resources
self.addEventListener('fetch', event => {
    // Only handle same-origin requests and critical CDN resources
    if (event.request.url.startsWith(self.location.origin) || 
        event.request.url.includes('cdn.jsdelivr.net') ||
        event.request.url.includes('cdnjs.cloudflare.com')) {
        
        event.respondWith(
            caches.match(event.request)
                .then(response => {
                    // Return cached version if available
                    if (response) {
                        return response;
                    }
                    
                    // Otherwise fetch from network
                    return fetch(event.request)
                        .then(response => {
                            // Cache successful responses for critical resources
                            if (response.status === 200 && 
                                (CRITICAL_RESOURCES.some(url => event.request.url.includes(url)) ||
                                 event.request.url.includes('.css') ||
                                 event.request.url.includes('.js'))) {
                                
                                const responseClone = response.clone();
                                caches.open(CACHE_NAME)
                                    .then(cache => {
                                        cache.put(event.request, responseClone);
                                    });
                            }
                            return response;
                        })
                        .catch(() => {
                            // Fallback for offline scenarios
                            if (event.request.destination === 'document') {
                                return caches.match('/');
                            }
                        });
                })
        );
    }
});
