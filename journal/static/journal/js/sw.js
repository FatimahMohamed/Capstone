// Service Worker for Gratitude Journal
// Caches critical resources to eliminate render blocking on repeat visits
/*global self, caches, console, Promise, fetch */

(function () {
    'use strict';

    var CACHE_NAME = 'gratitude-journal-v1',
        CRITICAL_RESOURCES = [
            '/',
            '/static/journal/css/style.css',
            '/static/journal/js/app.js',
            'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css',
            'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
        ];

    // Install event - cache critical resources
    self.addEventListener('install', function (event) {
        event.waitUntil(
            caches.open(CACHE_NAME)
                .then(function (cache) {
                    console.log('Caching critical resources');
                    return cache.addAll(CRITICAL_RESOURCES);
                })
                .catch(function (error) {
                    console.log('Cache install failed:', error);
                })
        );
        self.skipWaiting();
    });

    // Activate event - clean up old caches
    self.addEventListener('activate', function (event) {
        event.waitUntil(
            caches.keys().then(function (cacheNames) {
                return Promise.all(
                    cacheNames.map(function (cacheName) {
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
    self.addEventListener('fetch', function (event) {
        // Only handle same-origin requests and critical CDN resources
        if (event.request.url.indexOf(self.location.origin) === 0 ||
                event.request.url.indexOf('cdn.jsdelivr.net') !== -1 ||
                event.request.url.indexOf('cdnjs.cloudflare.com') !== -1) {

            event.respondWith(
                caches.match(event.request)
                    .then(function (response) {
                        // Return cached version if available
                        if (response) {
                            return response;
                        }

                        // Otherwise fetch from network
                        return fetch(event.request)
                            .then(function (networkResponse) {
                                var responseClone;
                                // Cache successful responses for critical resources
                                if (networkResponse.status === 200 &&
                                        (CRITICAL_RESOURCES.some(function (url) {
                                            return event.request.url.indexOf(url) !== -1;
                                        }) ||
                                            event.request.url.indexOf('.css') !== -1 ||
                                            event.request.url.indexOf('.js') !== -1)) {

                                    responseClone = networkResponse.clone();
                                    caches.open(CACHE_NAME)
                                        .then(function (cache) {
                                            cache.put(event.request, responseClone);
                                        });
                                }
                                return networkResponse;
                            })
                            .catch(function () {
                                // Fallback for offline scenarios
                                if (event.request.destination === 'document') {
                                    return caches.match('/');
                                }
                            });
                    })
            );
        }
    });

}());
