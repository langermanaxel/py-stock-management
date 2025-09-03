/**
 * Lazy Loader - Carga diferida de imágenes e íconos
 * Optimiza el rendimiento cargando contenido solo cuando es necesario
 */

class LazyLoader {
    constructor() {
        this.imageObserver = null;
        this.iconObserver = null;
        this.scriptObserver = null;
        this.loadedImages = new Set();
        this.loadedIcons = new Set();
        this.init();
    }

    init() {
        // Setup intersection observers
        this.setupImageObserver();
        this.setupIconObserver();
        this.setupScriptObserver();
        
        // Setup lazy loading for existing elements
        this.setupExistingElements();
        
        // Setup performance monitoring
        this.setupPerformanceMonitoring();
    }

    /**
     * Setup intersection observer for images
     */
    setupImageObserver() {
        if (!('IntersectionObserver' in window)) {
            // Fallback for older browsers
            this.loadAllImages();
            return;
        }

        this.imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.loadImage(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, {
            rootMargin: '50px 0px',
            threshold: 0.01
        });
    }

    /**
     * Setup intersection observer for icons
     */
    setupIconObserver() {
        if (!('IntersectionObserver' in window)) {
            this.loadAllIcons();
            return;
        }

        this.iconObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.loadIcon(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, {
            rootMargin: '20px 0px',
            threshold: 0.01
        });
    }

    /**
     * Setup intersection observer for scripts
     */
    setupScriptObserver() {
        if (!('IntersectionObserver' in window)) {
            return;
        }

        this.scriptObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.loadScript(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, {
            rootMargin: '100px 0px',
            threshold: 0.01
        });
    }

    /**
     * Setup lazy loading for existing elements
     */
    setupExistingElements() {
        // Setup images
        document.querySelectorAll('img[data-src]').forEach(img => {
            this.imageObserver?.observe(img);
        });

        // Setup icons
        document.querySelectorAll('svg[data-src], .icon[data-src]').forEach(icon => {
            this.iconObserver?.observe(icon);
        });

        // Setup scripts
        document.querySelectorAll('script[data-src]').forEach(script => {
            this.scriptObserver?.observe(script);
        });
    }

    /**
     * Load an image with optimizations
     */
    loadImage(img) {
        const src = img.getAttribute('data-src');
        if (!src || this.loadedImages.has(src)) return;

        // Add loading class
        img.classList.add('loading');
        
        // Create a new image to preload
        const newImg = new Image();
        
        newImg.onload = () => {
            img.src = src;
            img.removeAttribute('data-src');
            img.classList.remove('loading');
            img.classList.add('loaded');
            this.loadedImages.add(src);
            
            // Emit loaded event
            this.emitEvent('imageLoaded', { src, element: img });
        };
        
        newImg.onerror = () => {
            img.classList.remove('loading');
            img.classList.add('error');
            console.warn(`Failed to load image: ${src}`);
            
            // Emit error event
            this.emitEvent('imageError', { src, element: img });
        };
        
        // Optimize image source based on device capabilities
        const optimizedSrc = this.optimizeImageSrc(src);
        newImg.src = optimizedSrc;
    }

    /**
     * Load an icon with optimizations
     */
    loadIcon(icon) {
        const src = icon.getAttribute('data-src');
        if (!src || this.loadedIcons.has(src)) return;

        // Add loading class
        icon.classList.add('loading');
        
        // For SVG icons, we can load them as inline SVG
        if (src.endsWith('.svg')) {
            this.loadSVGIcon(icon, src);
        } else {
            // For other icon formats
            this.loadImageIcon(icon, src);
        }
    }

    /**
     * Load SVG icon as inline SVG
     */
    loadSVGIcon(icon, src) {
        fetch(src)
            .then(response => response.text())
            .then(svgText => {
                // Create a temporary container
                const temp = document.createElement('div');
                temp.innerHTML = svgText;
                const svg = temp.querySelector('svg');
                
                if (svg) {
                    // Copy attributes from original element
                    Array.from(icon.attributes).forEach(attr => {
                        if (attr.name !== 'data-src') {
                            svg.setAttribute(attr.name, attr.value);
                        }
                    });
                    
                    // Replace the original element
                    icon.parentNode.replaceChild(svg, icon);
                    this.loadedIcons.add(src);
                    
                    // Emit loaded event
                    this.emitEvent('iconLoaded', { src, element: svg });
                }
            })
            .catch(error => {
                icon.classList.remove('loading');
                icon.classList.add('error');
                console.warn(`Failed to load SVG icon: ${src}`, error);
            });
    }

    /**
     * Load image icon
     */
    loadImageIcon(icon, src) {
        const img = new Image();
        
        img.onload = () => {
            icon.style.backgroundImage = `url(${src})`;
            icon.removeAttribute('data-src');
            icon.classList.remove('loading');
            icon.classList.add('loaded');
            this.loadedIcons.add(src);
            
            // Emit loaded event
            this.emitEvent('iconLoaded', { src, element: icon });
        };
        
        img.onerror = () => {
            icon.classList.remove('loading');
            icon.classList.add('error');
            console.warn(`Failed to load icon: ${src}`);
        };
        
        img.src = src;
    }

    /**
     * Load a script when it comes into view
     */
    loadScript(script) {
        const src = script.getAttribute('data-src');
        if (!src) return;

        const newScript = document.createElement('script');
        newScript.src = src;
        newScript.defer = true;
        
        newScript.onload = () => {
            script.removeAttribute('data-src');
            script.classList.add('loaded');
            
            // Emit loaded event
            this.emitEvent('scriptLoaded', { src, element: script });
        };
        
        newScript.onerror = () => {
            script.classList.add('error');
            console.warn(`Failed to load script: ${src}`);
        };
        
        document.head.appendChild(newScript);
    }

    /**
     * Optimize image source based on device capabilities
     */
    optimizeImageSrc(src) {
        const devicePixelRatio = window.devicePixelRatio || 1;
        const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
        
        let optimizedSrc = src;
        
        // Adjust quality based on connection
        if (connection) {
            if (connection.effectiveType === 'slow-2g' || connection.effectiveType === '2g') {
                optimizedSrc = src.replace(/\.(jpg|jpeg|png)$/, '_low.$1');
            } else if (connection.effectiveType === '3g') {
                optimizedSrc = src.replace(/\.(jpg|jpeg|png)$/, '_medium.$1');
            }
        }
        
        // Adjust for high DPI displays
        if (devicePixelRatio > 1) {
            optimizedSrc = optimizedSrc.replace(/\.(jpg|jpeg|png)$/, '_2x.$1');
        }
        
        // Add WebP support if available
        if (this.supportsWebP()) {
            optimizedSrc = optimizedSrc.replace(/\.(jpg|jpeg|png)$/, '.webp');
        }
        
        return optimizedSrc;
    }

    /**
     * Check if browser supports WebP
     */
    supportsWebP() {
        const canvas = document.createElement('canvas');
        canvas.width = 1;
        canvas.height = 1;
        return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0;
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
     * Load all icons (fallback for older browsers)
     */
    loadAllIcons() {
        document.querySelectorAll('svg[data-src], .icon[data-src]').forEach(icon => {
            this.loadIcon(icon);
        });
    }

    /**
     * Setup performance monitoring
     */
    setupPerformanceMonitoring() {
        // Monitor image loading performance
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                entries.forEach(entry => {
                    if (entry.name.includes('/static/') && 
                        (entry.name.includes('.jpg') || entry.name.includes('.png') || entry.name.includes('.svg'))) {
                        this.reportMetric('image-load', entry.duration, { src: entry.name });
                    }
                });
            });
            
            observer.observe({ entryTypes: ['resource'] });
        }
    }

    /**
     * Report performance metrics
     */
    reportMetric(name, value, metadata = {}) {
        if (window.performanceManager) {
            window.performanceManager.reportMetric(name, value, metadata);
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
     * Preload critical images
     */
    preloadCriticalImages() {
        const criticalImages = [
            '/static/images/logo.png',
            '/static/images/hero-bg.jpg'
        ];

        criticalImages.forEach(src => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'image';
            link.href = src;
            document.head.appendChild(link);
        });
    }

    /**
     * Setup lazy loading for dynamically added elements
     */
    setupDynamicLazyLoading() {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        // Check for new images
                        const images = node.querySelectorAll ? node.querySelectorAll('img[data-src]') : [];
                        images.forEach(img => this.imageObserver?.observe(img));
                        
                        // Check for new icons
                        const icons = node.querySelectorAll ? node.querySelectorAll('svg[data-src], .icon[data-src]') : [];
                        icons.forEach(icon => this.iconObserver?.observe(icon));
                        
                        // Check for new scripts
                        const scripts = node.querySelectorAll ? node.querySelectorAll('script[data-src]') : [];
                        scripts.forEach(script => this.scriptObserver?.observe(script));
                    }
                });
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    /**
     * Get loading statistics
     */
    getLoadingStats() {
        return {
            loadedImages: this.loadedImages.size,
            loadedIcons: this.loadedIcons.size,
            totalImages: document.querySelectorAll('img[data-src]').length,
            totalIcons: document.querySelectorAll('svg[data-src], .icon[data-src]').length
        };
    }

    /**
     * Clean up resources
     */
    cleanup() {
        this.imageObserver?.disconnect();
        this.iconObserver?.disconnect();
        this.scriptObserver?.disconnect();
    }
}

// Initialize lazy loader
const lazyLoader = new LazyLoader();

// Export for use in other modules
if (typeof window !== 'undefined') {
    window.lazyLoader = lazyLoader;
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = LazyLoader;
}
