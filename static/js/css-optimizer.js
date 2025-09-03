/**
 * CSS Optimizer - Minificación y optimización de CSS
 * Remueve CSS no utilizado y optimiza el rendimiento
 */

class CSSOptimizer {
    constructor() {
        this.usedClasses = new Set();
        this.usedSelectors = new Set();
        this.criticalCSS = '';
        this.nonCriticalCSS = '';
        this.init();
    }

    init() {
        // Extract critical CSS
        this.extractCriticalCSS();
        
        // Setup CSS usage tracking
        this.setupUsageTracking();
        
        // Optimize CSS loading
        this.optimizeCSSLoading();
    }

    /**
     * Extract critical CSS for above-the-fold content
     */
    extractCriticalCSS() {
        const criticalSelectors = [
            // Layout
            '.header-layout',
            '.main-layout',
            '.content-area',
            '.button-layout',
            '.search-layout',
            '.mobile-btn',
            '.search-input',
            '.table-container',
            '.modal-layout',
            '.modal-content',
            '.form-layout',
            
            // Typography
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            '.text-xl', '.text-2xl', '.text-lg',
            '.font-semibold', '.font-bold',
            
            // Colors
            '.bg-white', '.bg-gray-100', '.bg-blue-600',
            '.text-gray-900', '.text-gray-600', '.text-white',
            
            // Spacing
            '.px-4', '.py-5', '.p-6', '.mb-6', '.gap-3', '.gap-4',
            
            // Flexbox/Grid
            '.flex', '.items-center', '.justify-between',
            '.grid', '.grid-cols-1', '.grid-cols-2',
            
            // Responsive
            '@media (max-width: 768px)',
            '@media (max-width: 480px)',
            
            // Components
            '.btn', '.btn--primary', '.btn--secondary',
            '.input', '.input--md',
            '.table', '.table--striped',
            '.card', '.modal'
        ];

        // This would typically be done at build time
        // For now, we'll mark these as critical
        this.criticalCSS = this.extractCSSForSelectors(criticalSelectors);
    }

    /**
     * Extract CSS for specific selectors
     */
    extractCSSForSelectors(selectors) {
        // This is a simplified version
        // In a real implementation, you'd parse the CSS and extract matching rules
        return `
            /* Critical CSS - Above the fold */
            .header-layout { display: flex; flex-direction: column; gap: 1rem; padding: 1rem; }
            .main-layout { display: grid; gap: 1.5rem; padding: 1rem; }
            .content-area { display: flex; flex-direction: column; gap: 1.5rem; }
            .button-layout { display: flex; flex-direction: column; gap: 0.75rem; }
            .search-layout { display: flex; flex-direction: column; gap: 1rem; padding: 1rem; }
            .mobile-btn { width: 100%; min-height: 48px; display: flex; align-items: center; justify-content: center; gap: 0.5rem; padding: 1rem; border: 1px solid transparent; border-radius: 0.5rem; background: #2563eb; color: white; font-size: 1rem; font-weight: 600; text-decoration: none; cursor: pointer; transition: background-color 0.2s; }
            .mobile-btn:hover { background: #1d4ed8; }
            .search-input { flex: 1; min-height: 48px; padding: 0.75rem 1rem; border: 1px solid #d1d5db; border-radius: 0.5rem; background: white; font-size: 1rem; transition: border-color 0.2s; }
            .search-input:focus { border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1); outline: none; }
            .table-container { overflow-x: auto; -webkit-overflow-scrolling: touch; }
            .modal-layout { position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 1000; display: flex; align-items: center; justify-content: center; padding: 1rem; background: rgba(0, 0, 0, 0.5); backdrop-filter: blur(4px); }
            .modal-content { width: 100%; max-width: 500px; max-height: 90vh; overflow-y: auto; background: white; border-radius: 1rem; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); border: 1px solid #e5e7eb; }
            .form-layout { display: flex; flex-direction: column; gap: 1rem; }
            
            @media (min-width: 768px) {
                .header-layout { flex-direction: row; align-items: center; justify-content: space-between; }
                .main-layout { grid-template-columns: 1fr 300px; padding: 1.5rem; }
                .button-layout { flex-direction: row; align-items: center; justify-content: flex-end; }
                .search-layout { flex-direction: row; align-items: center; justify-content: space-between; }
                .mobile-btn { width: auto; min-height: 40px; padding: 0.75rem 1.5rem; font-size: 0.875rem; }
                .search-input { min-width: 300px; font-size: 0.875rem; }
                .form-layout { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; }
            }
            
            @media (min-width: 1024px) {
                .main-layout { grid-template-columns: 1fr 350px; padding: 2rem; }
            }
        `;
    }

    /**
     * Setup CSS usage tracking
     */
    setupUsageTracking() {
        // Track class usage
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                    const classes = mutation.target.className.split(' ');
                    classes.forEach(cls => {
                        if (cls.trim()) {
                            this.usedClasses.add(cls.trim());
                        }
                    });
                }
            });
        });

        observer.observe(document.body, {
            attributes: true,
            subtree: true,
            attributeFilter: ['class']
        });

        // Track initial classes
        document.querySelectorAll('*').forEach(element => {
            if (element.className) {
                const classes = element.className.split(' ');
                classes.forEach(cls => {
                    if (cls.trim()) {
                        this.usedClasses.add(cls.trim());
                    }
                });
            }
        });
    }

    /**
     * Optimize CSS loading
     */
    optimizeCSSLoading() {
        // Load critical CSS inline
        this.injectCriticalCSS();
        
        // Load non-critical CSS asynchronously
        this.loadNonCriticalCSS();
        
        // Preload likely CSS
        this.preloadCSS();
    }

    /**
     * Inject critical CSS inline
     */
    injectCriticalCSS() {
        const style = document.createElement('style');
        style.textContent = this.criticalCSS;
        style.setAttribute('data-critical', 'true');
        document.head.insertBefore(style, document.head.firstChild);
    }

    /**
     * Load non-critical CSS asynchronously
     */
    loadNonCriticalCSS() {
        const cssFiles = [
            'design-tokens.css',
            'components.css',
            'responsive.css'
        ];

        cssFiles.forEach(cssFile => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'style';
            link.href = `/static/css/${cssFile}`;
            link.onload = () => {
                link.rel = 'stylesheet';
            };
            document.head.appendChild(link);
        });
    }

    /**
     * Preload likely CSS files
     */
    preloadCSS() {
        const likelyCSS = [
            'style.css'
        ];

        likelyCSS.forEach(cssFile => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'style';
            link.href = `/static/css/${cssFile}`;
            link.crossOrigin = 'anonymous';
            document.head.appendChild(link);
        });
    }

    /**
     * Remove unused CSS
     */
    removeUnusedCSS() {
        // This would typically be done at build time
        // For now, we'll just track usage
        console.log('Used classes:', Array.from(this.usedClasses));
    }

    /**
     * Optimize CSS for current view
     */
    optimizeForView(viewName) {
        const viewSpecificCSS = this.getViewSpecificCSS(viewName);
        
        if (viewSpecificCSS) {
            const style = document.createElement('style');
            style.textContent = viewSpecificCSS;
            style.setAttribute('data-view', viewName);
            document.head.appendChild(style);
        }
    }

    /**
     * Get view-specific CSS
     */
    getViewSpecificCSS(viewName) {
        const viewCSS = {
            'products': `
                .table-mobile-cards { display: grid; gap: 1rem; grid-template-columns: 1fr; }
                .mobile-card { background: white; border: 1px solid #e5e7eb; border-radius: 0.75rem; padding: 1rem; box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1); }
                .mobile-card__header { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem; padding-bottom: 0.75rem; border-bottom: 1px solid #e5e7eb; }
                .mobile-card__actions { display: flex; gap: 0.5rem; margin-top: 1rem; padding-top: 0.75rem; border-top: 1px solid #e5e7eb; }
            `,
            'dashboard': `
                .dashboard-widgets { display: grid; gap: 1.5rem; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); }
                .widget { background: white; border-radius: 0.75rem; padding: 1.5rem; box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1); }
            `,
            'stock': `
                .stock-levels { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); }
                .stock-item { background: white; border-radius: 0.5rem; padding: 1rem; border-left: 4px solid #3b82f6; }
            `
        };

        return viewCSS[viewName] || '';
    }

    /**
     * Minify CSS
     */
    minifyCSS(css) {
        return css
            .replace(/\/\*[\s\S]*?\*\//g, '') // Remove comments
            .replace(/\s+/g, ' ') // Replace multiple spaces with single space
            .replace(/;\s*}/g, '}') // Remove semicolon before closing brace
            .replace(/{\s+/g, '{') // Remove space after opening brace
            .replace(/;\s+/g, ';') // Remove space after semicolon
            .replace(/,\s+/g, ',') // Remove space after comma
            .replace(/:\s+/g, ':') // Remove space after colon
            .trim();
    }

    /**
     * Get CSS performance metrics
     */
    getPerformanceMetrics() {
        const stylesheets = Array.from(document.styleSheets);
        const metrics = {
            totalSheets: stylesheets.length,
            totalRules: 0,
            totalSize: 0,
            loadTime: 0
        };

        stylesheets.forEach(sheet => {
            try {
                if (sheet.cssRules) {
                    metrics.totalRules += sheet.cssRules.length;
                }
            } catch (e) {
                // Cross-origin stylesheets can't be accessed
            }
        });

        return metrics;
    }
}

// Initialize CSS optimizer
const cssOptimizer = new CSSOptimizer();

// Export for use in other modules
if (typeof window !== 'undefined') {
    window.cssOptimizer = cssOptimizer;
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = CSSOptimizer;
}
