// Service Worker - Cache Strategy
// Regional Veículos - Cache e Performance

const CACHE_NAME = 'regional-veiculos-v1.0.0';
const urlsToCache = [
    '/',
    '/estoque/',
    '/contato/',
    '/financiamento/',
    '/sobre/',
    '/static/css/style.css',
    '/static/js/main.js',
    '/static/js/analytics.js',
    '/static/js/performance.js',
    '/static/images/imagemcarr.jpg',
    '/static/images/logo-regional-veiculos.png',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
];

// Install event
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('[SW] Cache opened');
                return cache.addAll(urlsToCache);
            })
    );
});

// Fetch event - Network First for HTML, Cache First for assets
self.addEventListener('fetch', event => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Skip non-GET requests
    if (request.method !== 'GET') return;
    
    // Skip external domains (except CDNs)
    if (url.origin !== location.origin && 
        !url.host.includes('cdn.jsdelivr.net') && 
        !url.host.includes('cdnjs.cloudflare.com') &&
        !url.host.includes('fonts.googleapis.com') &&
        !url.host.includes('fonts.gstatic.com')) {
        return;
    }
    
    // HTML - Network First strategy
    if (request.headers.get('accept').includes('text/html')) {
        event.respondWith(
            fetch(request)
                .then(response => {
                    // Clone the response
                    const responseClone = response.clone();
                    
                    // Cache the new version
                    caches.open(CACHE_NAME)
                        .then(cache => {
                            cache.put(request, responseClone);
                        });
                    
                    return response;
                })
                .catch(() => {
                    // Fallback to cache
                    return caches.match(request);
                })
        );
    }
    // Static assets - Cache First strategy
    else if (request.url.includes('/static/') || 
             url.host.includes('cdn.') || 
             url.host.includes('fonts.')) {
        event.respondWith(
            caches.match(request)
                .then(response => {
                    // Return cached version if available
                    if (response) {
                        return response;
                    }
                    
                    // Fetch from network and cache
                    return fetch(request)
                        .then(response => {
                            // Don't cache if not ok
                            if (!response || response.status !== 200 || response.type !== 'basic') {
                                return response;
                            }
                            
                            const responseClone = response.clone();
                            
                            caches.open(CACHE_NAME)
                                .then(cache => {
                                    cache.put(request, responseClone);
                                });
                            
                            return response;
                        });
                })
        );
    }
    // Images - Cache First with fallback
    else if (request.url.includes('/media/') || 
             request.headers.get('accept').includes('image/')) {
        event.respondWith(
            caches.match(request)
                .then(response => {
                    if (response) {
                        return response;
                    }
                    
                    return fetch(request)
                        .then(response => {
                            if (response && response.status === 200) {
                                const responseClone = response.clone();
                                
                                caches.open(CACHE_NAME)
                                    .then(cache => {
                                        cache.put(request, responseClone);
                                    });
                            }
                            
                            return response;
                        })
                        .catch(() => {
                            // Return fallback image
                            return caches.match('/static/images/carro-padrao.jpg');
                        });
                })
        );
    }
});

// Activate event - Clean old caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('[SW] Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Background sync for analytics
self.addEventListener('sync', event => {
    if (event.tag === 'analytics-sync') {
        event.waitUntil(
            // Send queued analytics data
            console.log('[SW] Background sync: analytics')
        );
    }
});

// Push notifications (for future use)
self.addEventListener('push', event => {
    const options = {
        body: 'Novos carros chegaram na Regional Veículos!',
        icon: '/static/images/favicon-192x192.png',
        badge: '/static/images/favicon-72x72.png',
        data: {
            url: '/estoque/'
        }
    };
    
    event.waitUntil(
        self.registration.showNotification('Regional Veículos', options)
    );
});

// Handle notification clicks
self.addEventListener('notificationclick', event => {
    event.notification.close();
    
    event.waitUntil(
        clients.openWindow(event.notification.data.url)
    );
});
