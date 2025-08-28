// Mobile Menu Management System
class MobileMenuManager {
    constructor() {
        this.isOpen = false;
        this.init();
    }

    init() {
        document.addEventListener('DOMContentLoaded', () => {
            this.setupMobileMenu();
            this.setupResizeHandler();
        });
    }

    setupMobileMenu() {
        const hamburgerButton = document.getElementById('mobile-menu-button');
        const mobileMenu = document.getElementById('mobile-menu');
        const overlay = document.getElementById('mobile-menu-overlay');

        if (hamburgerButton) {
            hamburgerButton.addEventListener('click', () => {
                this.toggleMobileMenu();
            });
        }

        if (overlay) {
            overlay.addEventListener('click', () => {
                this.closeMobileMenu();
            });
        }

        // Close menu when clicking on menu items
        const menuItems = document.querySelectorAll('#mobile-menu a');
        menuItems.forEach(item => {
            item.addEventListener('click', () => {
                this.closeMobileMenu();
            });
        });
    }

    setupResizeHandler() {
        window.addEventListener('resize', () => {
            if (window.innerWidth >= 768 && this.isOpen) {
                this.closeMobileMenu();
            }
        });
    }

    toggleMobileMenu() {
        this.isOpen = !this.isOpen;
        this.updateMobileMenu();
    }

    openMobileMenu() {
        this.isOpen = true;
        this.updateMobileMenu();
    }

    closeMobileMenu() {
        this.isOpen = false;
        this.updateMobileMenu();
    }

    updateMobileMenu() {
        const mobileMenu = document.getElementById('mobile-menu');
        const overlay = document.getElementById('mobile-menu-overlay');
        const hamburgerButton = document.getElementById('mobile-menu-button');

        if (mobileMenu) {
            if (this.isOpen) {
                mobileMenu.classList.add('translate-x-0');
                mobileMenu.classList.remove('-translate-x-full');
                document.body.classList.add('overflow-hidden');
            } else {
                mobileMenu.classList.remove('translate-x-0');
                mobileMenu.classList.add('-translate-x-full');
                document.body.classList.remove('overflow-hidden');
            }
        }

        if (overlay) {
            if (this.isOpen) {
                overlay.classList.remove('hidden');
                overlay.classList.add('block');
            } else {
                overlay.classList.add('hidden');
                overlay.classList.remove('block');
            }
        }

        if (hamburgerButton) {
            const icon = hamburgerButton.querySelector('svg');
            if (icon) {
                if (this.isOpen) {
                    // X icon (close)
                    icon.innerHTML = `
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                              d="M6 18L18 6M6 6l12 12">
                        </path>
                    `;
                } else {
                    // Hamburger icon (menu)
                    icon.innerHTML = `
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                              d="M4 6h16M4 12h16M4 18h16">
                        </path>
                    `;
                }
            }
        }
    }

    isMobileMenuOpen() {
        return this.isOpen;
    }
}

// Initialize mobile menu manager
const mobileMenuManager = new MobileMenuManager();

// Export for use in other scripts
window.mobileMenuManager = mobileMenuManager;

// Alpine.js data for mobile menu management
window.mobileMenuData = () => ({
    isOpen: false,
    
    toggleMobileMenu() {
        mobileMenuManager.toggleMobileMenu();
        this.isOpen = mobileMenuManager.isMobileMenuOpen();
    },
    
    closeMobileMenu() {
        mobileMenuManager.closeMobileMenu();
        this.isOpen = mobileMenuManager.isMobileMenuOpen();
    }
});
