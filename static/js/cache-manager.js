/**
 * Cache Manager - Gestión de cache y headers de archivos estáticos
 * Optimiza el rendimiento con estrategias de cache inteligentes
 */

class CacheManager {
    constructor() {
        this.cacheStrategies = {
            'css': { maxAge: 31536000, immutable: true }, // 1 year
            'js': { maxAge: 31536000, immutable: true }, // 1 year
            'images': { maxAge: 2592000, immutable: true }, // 30 days
            'fonts': { maxAge: 31536000, immutable: true }, // 1 year
            'icons': { maxAge: 2592000, immutable: true }, // 30 days
            'html': { maxAge: 3600, immutable: false } // 1 hour
        };
        this.cacheStorage = null;
        this.init();
    }

    init() {
        // Setup service worker for advanced caching
        this.setupServiceWorker();
        
        // Setup cache headers
        this.setupCacheHeaders();
        
        // Setup cache strategies
        this.setupCacheStrategies();
        
        // Setup cache monitoring
        this.setupCacheMonitoring();
    }

    /**
     * Setup service worker for advanced caching
     */
    setupServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/static/js/sw.js')
                .then(registration => {
                    console.log('Service Worker registered:', registration);
                })
                .catch(error => {
                    console.log('Service Worker registration failed:', error);
                });
        }
    }

    /**
     * Setup cache headers for different file types
     */
    setupCacheHeaders() {
        // This would typically be done server-side
        // For now, we'll simulate the behavior
        
        const fileTypes = {
            '.css': 'css',
            '.js': 'js',
            '.png': 'images',
            '.jpg': 'images',
            '.jpeg': 'images',
            '.gif': 'images',
            '.svg': 'icons',
            '.woff': 'fonts',
            '.woff2': 'fonts',
            '.ttf': 'fonts',
            '.eot': 'fonts',
            '.html': 'html'
        };

        // Monitor resource loading and apply cache strategies
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                entries.forEach(entry => {
                    const fileType = this.getFileType(entry.name);
                    if (fileType) {
                        this.applyCacheStrategy(entry.name, fileType);
                    }
                });
            });
            
            observer.observe({ entryTypes: ['resource'] });
        }
    }

    /**
     * Get file type from URL
     */
    getFileType(url) {
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
        
        return fileTypes[extension];
    }

    /**
     * Apply cache strategy for a resource
     */
    applyCacheStrategy(url, fileType) {
        const strategy = this.cacheStrategies[fileType];
        if (!strategy) return;

        // In a real implementation, this would set HTTP headers
        // For now, we'll just log the strategy
        console.log(`Cache strategy for ${url}:`, strategy);
    }

    /**
     * Setup cache strategies
     */
    setupCacheStrategies() {
        // Cache critical resources
        this.cacheCriticalResources();
        
        // Setup cache invalidation
        this.setupCacheInvalidation();
        
        // Setup cache warming
        this.setupCacheWarming();
    }

    /**
     * Cache critical resources
     */
    cacheCriticalResources() {
        const criticalResources = [
            '/static/css/design-tokens.css',
            '/static/css/components.css',
            '/static/css/responsive.css',
            '/static/js/performance.js',
            '/static/js/accessibility.js',
            '/static/js/feedback.js',
            '/static/js/form-ux.js'
        ];

        criticalResources.forEach(resource => {
            this.preloadResource(resource);
        });
    }

    /**
     * Preload a resource
     */
    preloadResource(url) {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.href = url;
        
        // Determine resource type
        if (url.endsWith('.css')) {
            link.as = 'style';
        } else if (url.endsWith('.js')) {
            link.as = 'script';
        } else if (url.match(/\.(png|jpg|jpeg|gif|svg)$/)) {
            link.as = 'image';
        } else if (url.match(/\.(woff|woff2|ttf|eot)$/)) {
            link.as = 'font';
        }
        
        link.crossOrigin = 'anonymous';
        document.head.appendChild(link);
    }

    /**
     * Setup cache invalidation
     */
    setupCacheInvalidation() {
        // Listen for cache invalidation events
        document.addEventListener('cacheInvalidate', (event) => {
            const { type, resource } = event.detail;
            this.invalidateCache(type, resource);
        });
    }

    /**
     * Invalidate cache for a specific resource
     */
    invalidateCache(type, resource) {
        if (type === 'all') {
            this.clearAllCache();
        } else if (type === 'resource') {
            this.clearResourceCache(resource);
        } else if (type === 'type') {
            this.clearTypeCache(resource);
        }
    }

    /**
     * Clear all cache
     */
    clearAllCache() {
        if ('caches' in window) {
            caches.keys().then(cacheNames => {
                cacheNames.forEach(cacheName => {
                    caches.delete(cacheName);
                });
            });
        }
    }

    /**
     * Clear cache for a specific resource
     */
    clearResourceCache(resource) {
        if ('caches' in window) {
            caches.keys().then(cacheNames => {
                cacheNames.forEach(cacheName => {
                    caches.open(cacheName).then(cache => {
                        cache.delete(resource);
                    });
                });
            });
        }
    }

    /**
     * Clear cache for a specific file type
     */
    clearTypeCache(fileType) {
        if ('caches' in window) {
            caches.keys().then(cacheNames => {
                cacheNames.forEach(cacheName => {
                    caches.open(cacheName).then(cache => {
                        cache.keys().then(requests => {
                            requests.forEach(request => {
                                if (this.getFileType(request.url) === fileType) {
                                    cache.delete(request);
                                }
                            });
                        });
                    });
                });
            });
        }
    }

    /**
     * Setup cache warming
     */
    setupCacheWarming() {
        // Warm cache for likely next resources
        this.warmCacheForCurrentView();
        
        // Warm cache on user interaction
        this.setupInteractionBasedWarming();
    }

    /**
     * Warm cache for current view
     */
    warmCacheForCurrentView() {
        const currentView = this.getCurrentView();
        const likelyResources = this.getLikelyResources(currentView);
        
        likelyResources.forEach(resource => {
            this.preloadResource(resource);
        });
    }

    /**
     * Get current view
     */
    getCurrentView() {
        const path = window.location.pathname;
        const viewMap = {
            '/products': 'products',
            '/dashboard': 'dashboard',
            '/stock': 'stock',
            '/categories': 'categories',
            '/orders': 'orders',
            '/purchases': 'purchases',
            '/users': 'users',
            '/login': 'login'
        };
        
        return viewMap[path] || 'dashboard';
    }

    /**
     * Get likely resources for a view
     */
    getLikelyResources(view) {
        const resourceMap = {
            'products': [
                '/static/js/table-manager.js',
                '/static/js/responsive-tables.js'
            ],
            'dashboard': [
                '/static/js/dashboard-charts.js',
                '/static/js/dashboard-widgets.js'
            ],
            'stock': [
                '/static/js/stock-manager.js',
                '/static/js/inventory-tracker.js'
            ],
            'categories': [
                '/static/js/category-manager.js'
            ],
            'orders': [
                '/static/js/order-manager.js',
                '/static/js/order-tracking.js'
            ],
            'purchases': [
                '/static/js/purchase-manager.js',
                '/static/js/supplier-manager.js'
            ],
            'users': [
                '/static/js/user-manager.js',
                '/static/js/role-manager.js'
            ]
        };
        
        return resourceMap[view] || [];
    }

    /**
     * Setup interaction-based cache warming
     */
    setupInteractionBasedWarming() {
        // Warm cache on hover
        document.addEventListener('mouseover', (event) => {
            const link = event.target.closest('a[href]');
            if (link) {
                const href = link.getAttribute('href');
                if (href.startsWith('/')) {
                    this.warmCacheForView(href);
                }
            }
        });
    }

    /**
     * Warm cache for a specific view
     */
    warmCacheForView(viewPath) {
        const view = this.getViewFromPath(viewPath);
        const resources = this.getLikelyResources(view);
        
        resources.forEach(resource => {
            this.preloadResource(resource);
        });
    }

    /**
     * Get view from path
     */
    getViewFromPath(path) {
        const pathMap = {
            '/products': 'products',
            '/dashboard': 'dashboard',
            '/stock': 'stock',
            '/categories': 'categories',
            '/orders': 'orders',
            '/purchases': 'purchases',
            '/users': 'users',
            '/login': 'login'
        };
        
        return pathMap[path] || 'dashboard';
    }

    /**
     * Setup cache monitoring
     */
    setupCacheMonitoring() {
        // Monitor cache hit rates
        this.monitorCacheHitRates();
        
        // Monitor cache size
        this.monitorCacheSize();
    }

    /**
     * Monitor cache hit rates
     */
    monitorCacheHitRates() {
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                entries.forEach(entry => {
                    if (entry.transferSize === 0 && entry.decodedBodySize > 0) {
                        // This indicates a cache hit
                        this.reportCacheHit(entry.name);
                    }
                });
            });
            
            observer.observe({ entryTypes: ['resource'] });
        }
    }

    /**
     * Report cache hit
     */
    reportCacheHit(resource) {
        if (window.performanceManager) {
            window.performanceManager.reportMetric('cache-hit', 1, { resource });
        }
    }

    /**
     * Monitor cache size
     */
    monitorCacheSize() {
        if ('caches' in window) {
            setInterval(() => {
                caches.keys().then(cacheNames => {
                    let totalSize = 0;
                    cacheNames.forEach(cacheName => {
                        caches.open(cacheName).then(cache => {
                            cache.keys().then(requests => {
                                totalSize += requests.length;
                            });
                        });
                    });
                    
                    if (window.performanceManager) {
                        window.performanceManager.reportMetric('cache-size', totalSize);
                    }
                });
            }, 30000); // Check every 30 seconds
        }
    }

    /**
     * Get cache statistics
     */
    getCacheStats() {
        return new Promise((resolve) => {
            if (!('caches' in window)) {
                resolve({ error: 'Cache API not supported' });
                return;
            }
            
            caches.keys().then(cacheNames => {
                const stats = {
                    cacheNames: cacheNames,
                    totalCaches: cacheNames.length
                };
                
                resolve(stats);
            });
        });
    }

    /**
     * Optimize cache for current device
     */
    optimizeForDevice() {
        const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
        
        if (connection) {
            if (connection.effectiveType === 'slow-2g' || connection.effectiveType === '2g') {
                // Reduce cache size for slow connections
                this.reduceCacheSize();
            } else if (connection.effectiveType === '4g') {
                // Increase cache size for fast connections
                this.increaseCacheSize();
            }
        }
    }

    /**
     * Reduce cache size
     */
    reduceCacheSize() {
        // Implement cache size reduction logic
        console.log('Reducing cache size for slow connection');
    }

    /**
     * Increase cache size
     */
    increaseCacheSize() {
        // Implement cache size increase logic
        console.log('Increasing cache size for fast connection');
    }
}

// Initialize cache manager
const cacheManager = new CacheManager();

// Export for use in other modules
if (typeof window !== 'undefined') {
    window.cacheManager = cacheManager;
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = CacheManager;
}
