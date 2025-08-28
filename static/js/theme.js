// Theme Management System
class ThemeManager {
    constructor() {
        this.theme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        // Apply theme on page load
        this.applyTheme();
        
        // Listen for theme toggle events
        document.addEventListener('DOMContentLoaded', () => {
            this.setupThemeToggle();
        });
    }

    applyTheme() {
        const root = document.documentElement;
        
        if (this.theme === 'dark') {
            root.classList.add('dark');
            document.body.classList.add('dark-mode');
        } else {
            root.classList.remove('dark');
            document.body.classList.remove('dark-mode');
        }
    }

    toggleTheme() {
        this.theme = this.theme === 'light' ? 'dark' : 'light';
        localStorage.setItem('theme', this.theme);
        this.applyTheme();
        
        // Dispatch custom event for other components
        document.dispatchEvent(new CustomEvent('themeChanged', { 
            detail: { theme: this.theme } 
        }));
    }

    getCurrentTheme() {
        return this.theme;
    }

    setupThemeToggle() {
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                this.toggleTheme();
                this.updateToggleIcon();
            });
            this.updateToggleIcon();
        }
    }

    updateToggleIcon() {
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            const icon = themeToggle.querySelector('svg');
            if (icon) {
                if (this.theme === 'dark') {
                    // Sun icon for dark mode
                    icon.innerHTML = `
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                              d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z">
                        </path>
                    `;
                } else {
                    // Moon icon for light mode
                    icon.innerHTML = `
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                              d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z">
                        </path>
                    `;
                }
            }
        }
    }
}

// Initialize theme manager
const themeManager = new ThemeManager();

// Export for use in other scripts
window.themeManager = themeManager;

// Alpine.js data for theme management
window.themeData = () => ({
    theme: themeManager.getCurrentTheme(),
    
    toggleTheme() {
        themeManager.toggleTheme();
        this.theme = themeManager.getCurrentTheme();
    },
    
    get isDark() {
        return this.theme === 'dark';
    }
});
