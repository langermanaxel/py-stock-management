/**
 * Performance Manager - Gestión de rendimiento y carga optimizada
 * Split de JavaScript por vistas, lazy loading y optimizaciones
 */

class PerformanceManager {
    constructor() {
        this.loadedViews = new Set();
        this.loadingViews = new Set();
        this.viewScripts = {
            'products': [
                'table-manager.js',
                'responsive-tables.js'
            ],
            'dashboard': [
                'dashboard-charts.js',
                'dashboard-widgets.js'
            ],
            'stock': [
                'stock-manager.js',
                'inventory-tracker.js'
            ],
            'categories': [
                'category-manager.js'
            ],
            'orders': [
                'order-manager.js',
                'order-tracking.js'
            ],
            'purchases': [
                'purchase-manager.js',
                'supplier-manager.js'
            ],
            'users': [
                'user-manager.js',
                'role-manager.js'
            ],
            'login': [
                'login-validation.js'
            ]
        };
        this.criticalScripts = [
            'accessibility.js',
            'feedback.js',
            'form-ux.js'
        ];
        this.init();
    }

    init() {
        // Load critical scripts immediately
        this.loadCriticalScripts();
        
        // Setup intersection observer for lazy loading
        this.setupLazyLoading();
        
        // Setup performance monitoring
        this.setupPerformanceMonitoring();
        
        // Preload next likely scripts
        this.preloadNextScripts();
    }

    /**
     * Load critical scripts that are needed immediately
     */
    loadCriticalScripts() {
        this.criticalScripts.forEach(scriptName => {
            this.loadScript(scriptName, { critical: true });
        });
    }

    /**
     * Load view-specific scripts
     */
    async loadViewScripts(viewName) {
        if (this.loadedViews.has(viewName) || this.loadingViews.has(viewName)) {
            return;
        }

        this.loadingViews.add(viewName);
        
        const scripts = this.viewScripts[viewName] || [];
        
        try {
            // Load scripts in parallel for better performance
            const loadPromises = scripts.map(scriptName => 
                this.loadScript(scriptName, { view: viewName })
            );
            
            await Promise.all(loadPromises);
            
            this.loadedViews.add(viewName);
            this.loadingViews.delete(viewName);
            
            // Emit event for view scripts loaded
            this.emitEvent('viewScriptsLoaded', { view: viewName });
            
        } catch (error) {
            console.error(`Error loading scripts for view ${viewName}:`, error);
            this.loadingViews.delete(viewName);
        }
    }

    /**
     * Load a single script with optimizations
     */
    loadScript(scriptName, options = {}) {
        return new Promise((resolve, reject) => {
            // Check if script is already loaded
            if (document.querySelector(`script[src*="${scriptName}"]`)) {
                resolve();
                return;
            }

            const script = document.createElement('script');
            script.src = `/static/js/${scriptName}`;
            script.defer = true;
            
            // Add performance attributes
            if (options.critical) {
                script.setAttribute('data-critical', 'true');
            }
            
            if (options.view) {
                script.setAttribute('data-view', options.view);
            }
            
            // Add loading attribute for better performance
            script.setAttribute('loading', 'lazy');
            
            // Add crossorigin for better caching
            script.crossOrigin = 'anonymous';
            
            script.onload = () => {
                resolve();
            };
            
            script.onerror = () => {
                reject(new Error(`Failed to load script: ${scriptName}`));
            };
            
            document.head.appendChild(script);
        });
    }

    /**
     * Setup lazy loading for images and icons
     */
    setupLazyLoading() {
        // Use Intersection Observer for better performance
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        this.loadImage(img);
                        observer.unobserve(img);
                    }
                });
            }, {
                rootMargin: '50px 0px',
                threshold: 0.01
            });

            // Observe all images with data-src
            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });

            // Observe all SVGs with data-src
            document.querySelectorAll('svg[data-src]').forEach(svg => {
                imageObserver.observe(svg);
            });
        } else {
            // Fallback for older browsers
            this.loadAllImages();
        }
    }

    /**
     * Load an image with optimizations
     */
    loadImage(img) {
        const src = img.getAttribute('data-src');
        if (!src) return;

        // Create a new image to preload
        const newImg = new Image();
        
        newImg.onload = () => {
            img.src = src;
            img.removeAttribute('data-src');
            img.classList.add('loaded');
        };
        
        newImg.onerror = () => {
            img.classList.add('error');
            console.warn(`Failed to load image: ${src}`);
        };
        
        newImg.src = src;
    }

    /**
     * Load all images (fallback for older browsers)
     */
    loadAllImages() {
        document.querySelectorAll('img[data-src]').forEach(img => {
            this.loadImage(img);
        });
    }

    /**
     * Preload next likely scripts based on current view
     */
    preloadNextScripts() {
        const currentView = this.getCurrentView();
        const nextViews = this.getNextLikelyViews(currentView);
        
        nextViews.forEach(viewName => {
            const scripts = this.viewScripts[viewName] || [];
            scripts.forEach(scriptName => {
                this.preloadScript(scriptName);
            });
        });
    }

    /**
     * Preload a script without executing it
     */
    preloadScript(scriptName) {
        if (document.querySelector(`link[rel="preload"][href*="${scriptName}"]`)) {
            return;
        }

        const link = document.createElement('link');
        link.rel = 'preload';
        link.as = 'script';
        link.href = `/static/js/${scriptName}`;
        link.crossOrigin = 'anonymous';
        
        document.head.appendChild(link);
    }

    /**
     * Get current view name from URL
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
     * Get next likely views based on current view
     */
    getNextLikelyViews(currentView) {
        const likelyViews = {
            'dashboard': ['products', 'stock'],
            'products': ['stock', 'categories'],
            'stock': ['products', 'orders'],
            'categories': ['products'],
            'orders': ['stock', 'purchases'],
            'purchases': ['orders', 'users'],
            'users': ['dashboard'],
            'login': ['dashboard']
        };
        
        return likelyViews[currentView] || [];
    }

    /**
     * Setup performance monitoring
     */
    setupPerformanceMonitoring() {
        // Monitor Core Web Vitals
        if ('PerformanceObserver' in window) {
            // Largest Contentful Paint
            new PerformanceObserver((list) => {
                const entries = list.getEntries();
                const lastEntry = entries[entries.length - 1];
                this.reportMetric('LCP', lastEntry.startTime);
            }).observe({ entryTypes: ['largest-contentful-paint'] });

            // First Input Delay
            new PerformanceObserver((list) => {
                const entries = list.getEntries();
                entries.forEach(entry => {
                    this.reportMetric('FID', entry.processingStart - entry.startTime);
                });
            }).observe({ entryTypes: ['first-input'] });

            // Cumulative Layout Shift
            new PerformanceObserver((list) => {
                let clsValue = 0;
                const entries = list.getEntries();
                entries.forEach(entry => {
                    if (!entry.hadRecentInput) {
                        clsValue += entry.value;
                    }
                });
                this.reportMetric('CLS', clsValue);
            }).observe({ entryTypes: ['layout-shift'] });
        }

        // Monitor script loading times
        this.monitorScriptLoading();
    }

    /**
     * Monitor script loading performance
     */
    monitorScriptLoading() {
        const observer = new PerformanceObserver((list) => {
            const entries = list.getEntries();
            entries.forEach(entry => {
                if (entry.name.includes('/static/js/')) {
                    const scriptName = entry.name.split('/').pop();
                    this.reportMetric('script-load', entry.duration, { script: scriptName });
                }
            });
        });
        
        observer.observe({ entryTypes: ['resource'] });
    }

    /**
     * Report performance metrics
     */
    reportMetric(name, value, metadata = {}) {
        // Send to analytics or logging service
        if (window.gtag) {
            window.gtag('event', 'performance_metric', {
                metric_name: name,
                metric_value: value,
                ...metadata
            });
        }
        
        // Log to console in development
        if (process.env.NODE_ENV === 'development') {
            console.log(`Performance Metric - ${name}:`, value, metadata);
        }
    }

    /**
     * Emit custom events
     */
    emitEvent(eventName, data) {
        const event = new CustomEvent(eventName, { detail: data });
        document.dispatchEvent(event);
    }

    /**
     * Optimize images based on device capabilities
     */
    optimizeImages() {
        const images = document.querySelectorAll('img[data-src]');
        const devicePixelRatio = window.devicePixelRatio || 1;
        const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
        
        images.forEach(img => {
            let src = img.getAttribute('data-src');
            
            // Adjust quality based on connection
            if (connection) {
                if (connection.effectiveType === 'slow-2g' || connection.effectiveType === '2g') {
                    src = src.replace(/\.(jpg|jpeg|png)$/, '_low.$1');
                } else if (connection.effectiveType === '3g') {
                    src = src.replace(/\.(jpg|jpeg|png)$/, '_medium.$1');
                }
            }
            
            // Adjust for high DPI displays
            if (devicePixelRatio > 1) {
                src = src.replace(/\.(jpg|jpeg|png)$/, '_2x.$1');
            }
            
            img.setAttribute('data-src', src);
        });
    }

    /**
     * Clean up resources
     */
    cleanup() {
        // Remove event listeners
        // Clear timeouts/intervals
        // Clean up observers
    }
}

// Initialize performance manager
const performanceManager = new PerformanceManager();

// Export for use in other modules
if (typeof window !== 'undefined') {
    window.performanceManager = performanceManager;
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = PerformanceManager;
}
