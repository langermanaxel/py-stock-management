/**
 * Service Worker - Cache avanzado y estrategias de red
 * Implementa cache-first, network-first y otras estrategias
 */

const CACHE_NAME = 'stock-management-v1';
const STATIC_CACHE = 'static-v1';
const DYNAMIC_CACHE = 'dynamic-v1';

// Resources to cache immediately
const STATIC_RESOURCES = [
    '/static/css/design-tokens.css',
    '/static/css/components.css',
    '/static/css/responsive.css',
    '/static/js/performance.js',
    '/static/js/accessibility.js',
    '/static/js/feedback.js',
    '/static/js/form-ux.js',
    '/static/js/lazy-loader.js',
    '/static/js/cache-manager.js'
];

// Resources to cache on demand
const DYNAMIC_RESOURCES = [
    '/static/js/table-manager.js',
    '/static/js/responsive-tables.js',
    '/static/js/dashboard-charts.js',
    '/static/js/stock-manager.js',
    '/static/js/category-manager.js',
    '/static/js/order-manager.js',
    '/static/js/purchase-manager.js',
    '/static/js/user-manager.js'
];

// Install event - cache static resources
self.addEventListener('install', (event) => {
    console.log('Service Worker installing...');
    
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then(cache => {
                console.log('Caching static resources...');
                return cache.addAll(STATIC_RESOURCES);
            })
            .then(() => {
                console.log('Static resources cached successfully');
                return self.skipWaiting();
            })
            .catch(error => {
                console.error('Error caching static resources:', error);
            })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    console.log('Service Worker activating...');
    
    event.waitUntil(
        caches.keys()
            .then(cacheNames => {
                return Promise.all(
                    cacheNames.map(cacheName => {
                        if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
                            console.log('Deleting old cache:', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            })
            .then(() => {
                console.log('Service Worker activated');
                return self.clients.claim();
            })
    );
});

// Fetch event - implement caching strategies
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }
    
    // Skip cross-origin requests
    if (url.origin !== location.origin) {
        return;
    }
    
    // Apply different strategies based on resource type
    if (isStaticResource(request.url)) {
        event.respondWith(cacheFirstStrategy(request));
    } else if (isDynamicResource(request.url)) {
        event.respondWith(networkFirstStrategy(request));
    } else if (isAPIRequest(request.url)) {
        event.respondWith(networkFirstStrategy(request));
    } else if (isHTMLRequest(request.url)) {
        event.respondWith(networkFirstStrategy(request));
    } else {
        event.respondWith(staleWhileRevalidateStrategy(request));
    }
});

// Cache First Strategy - for static resources
async function cacheFirstStrategy(request) {
    try {
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            const cache = await caches.open(STATIC_CACHE);
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.error('Cache first strategy failed:', error);
        return new Response('Resource not available', { status: 503 });
    }
}

// Network First Strategy - for dynamic content
async function networkFirstStrategy(request) {
    try {
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            const cache = await caches.open(DYNAMIC_CACHE);
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    } catch (error) {
        console.log('Network failed, trying cache:', error);
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        return new Response('Resource not available', { status: 503 });
    }
}

// Stale While Revalidate Strategy - for images and other resources
async function staleWhileRevalidateStrategy(request) {
    const cache = await caches.open(DYNAMIC_CACHE);
    const cachedResponse = await cache.match(request);
    
    const fetchPromise = fetch(request).then(networkResponse => {
        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    }).catch(error => {
        console.log('Network request failed:', error);
        return cachedResponse;
    });
    
    return cachedResponse || fetchPromise;
}

// Helper functions to determine resource types
function isStaticResource(url) {
    return url.includes('/static/css/') || 
           url.includes('/static/js/performance.js') ||
           url.includes('/static/js/accessibility.js') ||
           url.includes('/static/js/feedback.js') ||
           url.includes('/static/js/form-ux.js');
}

function isDynamicResource(url) {
    return url.includes('/static/js/table-manager.js') ||
           url.includes('/static/js/responsive-tables.js') ||
           url.includes('/static/js/dashboard-charts.js') ||
           url.includes('/static/js/stock-manager.js') ||
           url.includes('/static/js/category-manager.js') ||
           url.includes('/static/js/order-manager.js') ||
           url.includes('/static/js/purchase-manager.js') ||
           url.includes('/static/js/user-manager.js');
}

function isAPIRequest(url) {
    return url.includes('/api/');
}

function isHTMLRequest(url) {
    return url.endsWith('.html') || 
           (!url.includes('/static/') && !url.includes('/api/'));
}

// Message handling for cache management
self.addEventListener('message', (event) => {
    const { type, data } = event.data;
    
    switch (type) {
        case 'CACHE_INVALIDATE':
            handleCacheInvalidation(data);
            break;
        case 'CACHE_WARM':
            handleCacheWarming(data);
            break;
        case 'GET_CACHE_STATS':
            handleGetCacheStats(event);
            break;
        default:
            console.log('Unknown message type:', type);
    }
});

// Handle cache invalidation
async function handleCacheInvalidation(data) {
    const { type, resource } = data;
    
    if (type === 'all') {
        await caches.delete(STATIC_CACHE);
        await caches.delete(DYNAMIC_CACHE);
        console.log('All caches cleared');
    } else if (type === 'resource' && resource) {
        const cache = await caches.open(DYNAMIC_CACHE);
        await cache.delete(resource);
        console.log('Resource cache cleared:', resource);
    } else if (type === 'type' && resource) {
        const cache = await caches.open(DYNAMIC_CACHE);
        const requests = await cache.keys();
        
        for (const request of requests) {
            if (getFileType(request.url) === resource) {
                await cache.delete(request);
            }
        }
        console.log('Cache type cleared:', resource);
    }
}

// Handle cache warming
async function handleCacheWarming(data) {
    const { resources } = data;
    
    if (resources && Array.isArray(resources)) {
        const cache = await caches.open(DYNAMIC_CACHE);
        
        for (const resource of resources) {
            try {
                const response = await fetch(resource);
                if (response.ok) {
                    await cache.put(resource, response);
                    console.log('Resource warmed:', resource);
                }
            } catch (error) {
                console.error('Failed to warm resource:', resource, error);
            }
        }
    }
}

// Handle get cache stats
async function handleGetCacheStats(event) {
    try {
        const staticCache = await caches.open(STATIC_CACHE);
        const dynamicCache = await caches.open(DYNAMIC_CACHE);
        
        const staticRequests = await staticCache.keys();
        const dynamicRequests = await dynamicCache.keys();
        
        const stats = {
            staticCache: {
                name: STATIC_CACHE,
                size: staticRequests.length,
                resources: staticRequests.map(req => req.url)
            },
            dynamicCache: {
                name: DYNAMIC_CACHE,
                size: dynamicRequests.length,
                resources: dynamicRequests.map(req => req.url)
            }
        };
        
        event.ports[0].postMessage({ type: 'CACHE_STATS', data: stats });
    } catch (error) {
        event.ports[0].postMessage({ type: 'CACHE_STATS_ERROR', error: error.message });
    }
}

// Helper function to get file type
function getFileType(url) {
    const extension = url.split('.').pop().split('?')[0];
    const fileTypes = {
        'css': 'css',
        'js': 'js',
        'png': 'images',
        'jpg': 'images',
        'jpeg': 'images',
        'gif': 'images',
        'svg': 'icons',
        'woff': 'fonts',
        'woff2': 'fonts',
        'ttf': 'fonts',
        'eot': 'fonts',
        'html': 'html'
    };
    
    return fileTypes[extension] || 'unknown';
}

// Background sync for offline actions
self.addEventListener('sync', (event) => {
    if (event.tag === 'background-sync') {
        event.waitUntil(doBackgroundSync());
    }
});

// Perform background sync
async function doBackgroundSync() {
    try {
        // Implement background sync logic
        console.log('Performing background sync...');
        
        // Example: sync offline data
        const offlineData = await getOfflineData();
        if (offlineData.length > 0) {
            await syncOfflineData(offlineData);
        }
        
        console.log('Background sync completed');
    } catch (error) {
        console.error('Background sync failed:', error);
    }
}

// Get offline data from IndexedDB
async function getOfflineData() {
    // Implement IndexedDB access
    return [];
}

// Sync offline data with server
async function syncOfflineData(data) {
    // Implement data synchronization
    console.log('Syncing offline data:', data);
}

// Push notification handling
self.addEventListener('push', (event) => {
    if (event.data) {
        const data = event.data.json();
        const options = {
            body: data.body,
            icon: '/static/images/icon-192x192.png',
            badge: '/static/images/badge-72x72.png',
            vibrate: [100, 50, 100],
            data: {
                dateOfArrival: Date.now(),
                primaryKey: data.primaryKey
            },
            actions: [
                {
                    action: 'explore',
                    title: 'Ver detalles',
                    icon: '/static/images/checkmark.png'
                },
                {
                    action: 'close',
                    title: 'Cerrar',
                    icon: '/static/images/xmark.png'
                }
            ]
        };
        
        event.waitUntil(
            self.registration.showNotification(data.title, options)
        );
    }
});

// Notification click handling
self.addEventListener('notificationclick', (event) => {
    event.notification.close();
    
    if (event.action === 'explore') {
        event.waitUntil(
            clients.openWindow('/dashboard')
        );
    }
});

console.log('Service Worker loaded successfully');
