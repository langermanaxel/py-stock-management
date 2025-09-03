/**
 * Accessibility utilities for keyboard navigation and focus management
 */

class AccessibilityManager {
    constructor() {
        this.focusableElements = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
        this.init();
    }

    init() {
        this.setupSkipLinks();
        this.setupKeyboardNavigation();
        this.setupFocusTraps();
        this.setupAriaLiveRegions();
    }

    /**
     * Setup skip links functionality
     */
    setupSkipLinks() {
        const skipLinks = document.querySelectorAll('.skip-link');
        skipLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('href'));
                if (target) {
                    target.focus();
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    }

    /**
     * Setup keyboard navigation for dropdowns and modals
     */
    setupKeyboardNavigation() {
        // Handle Escape key for modals and dropdowns
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeOpenModals();
                this.closeOpenDropdowns();
            }
        });

        // Handle Enter and Space for custom buttons
        document.addEventListener('keydown', (e) => {
            if ((e.key === 'Enter' || e.key === ' ') && e.target.getAttribute('role') === 'button') {
                e.preventDefault();
                e.target.click();
            }
        });
    }

    /**
     * Setup focus traps for modals
     */
    setupFocusTraps() {
        const modals = document.querySelectorAll('[role="dialog"]');
        modals.forEach(modal => {
            this.createFocusTrap(modal);
        });
    }

    /**
     * Create focus trap for a modal
     */
    createFocusTrap(modal) {
        const focusableElements = modal.querySelectorAll(this.focusableElements);
        const firstFocusableElement = focusableElements[0];
        const lastFocusableElement = focusableElements[focusableElements.length - 1];

        modal.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                if (e.shiftKey) {
                    // Shift + Tab
                    if (document.activeElement === firstFocusableElement) {
                        e.preventDefault();
                        lastFocusableElement.focus();
                    }
                } else {
                    // Tab
                    if (document.activeElement === lastFocusableElement) {
                        e.preventDefault();
                        firstFocusableElement.focus();
                    }
                }
            }
        });
    }

    /**
     * Setup ARIA live regions for announcements
     */
    setupAriaLiveRegions() {
        // Create live region if it doesn't exist
        if (!document.getElementById('aria-live-region')) {
            const liveRegion = document.createElement('div');
            liveRegion.id = 'aria-live-region';
            liveRegion.setAttribute('aria-live', 'polite');
            liveRegion.setAttribute('aria-atomic', 'true');
            liveRegion.className = 'sr-only';
            document.body.appendChild(liveRegion);
        }
    }

    /**
     * Announce message to screen readers
     */
    announce(message) {
        const liveRegion = document.getElementById('aria-live-region');
        if (liveRegion) {
            liveRegion.textContent = message;
            // Clear after announcement
            setTimeout(() => {
                liveRegion.textContent = '';
            }, 1000);
        }
    }

    /**
     * Close all open modals
     */
    closeOpenModals() {
        const modals = document.querySelectorAll('[role="dialog"]');
        modals.forEach(modal => {
            if (modal.style.display !== 'none' && !modal.classList.contains('hidden')) {
                // Trigger close event
                const closeEvent = new CustomEvent('close-modal');
                modal.dispatchEvent(closeEvent);
            }
        });
    }

    /**
     * Close all open dropdowns
     */
    closeOpenDropdowns() {
        const dropdowns = document.querySelectorAll('[role="menu"]');
        dropdowns.forEach(dropdown => {
            if (dropdown.style.display !== 'none' && !dropdown.classList.contains('hidden')) {
                // Trigger close event
                const closeEvent = new CustomEvent('close-dropdown');
                dropdown.dispatchEvent(closeEvent);
            }
        });
    }

    /**
     * Get all focusable elements within a container
     */
    getFocusableElements(container) {
        return container.querySelectorAll(this.focusableElements);
    }

    /**
     * Focus first focusable element in container
     */
    focusFirst(container) {
        const focusableElements = this.getFocusableElements(container);
        if (focusableElements.length > 0) {
            focusableElements[0].focus();
        }
    }

    /**
     * Focus last focusable element in container
     */
    focusLast(container) {
        const focusableElements = this.getFocusableElements(container);
        if (focusableElements.length > 0) {
            focusableElements[focusableElements.length - 1].focus();
        }
    }

    /**
     * Validate form accessibility
     */
    validateFormAccessibility(form) {
        const inputs = form.querySelectorAll('input, select, textarea');
        let isValid = true;
        const errors = [];

        inputs.forEach(input => {
            const label = form.querySelector(`label[for="${input.id}"]`);
            if (!label && !input.getAttribute('aria-label') && !input.getAttribute('aria-labelledby')) {
                isValid = false;
                errors.push(`Input ${input.id || input.name} lacks proper labeling`);
            }

            if (input.hasAttribute('required') && !input.getAttribute('aria-required')) {
                input.setAttribute('aria-required', 'true');
            }
        });

        return { isValid, errors };
    }

    /**
     * Setup form validation with accessible error messages
     */
    setupFormValidation(form) {
        const inputs = form.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            input.addEventListener('blur', () => {
                this.validateInput(input);
            });

            input.addEventListener('input', () => {
                this.clearInputError(input);
            });
        });
    }

    /**
     * Validate individual input
     */
    validateInput(input) {
        const value = input.value.trim();
        const isRequired = input.hasAttribute('required');
        const minLength = input.getAttribute('minlength');
        const maxLength = input.getAttribute('maxlength');
        const pattern = input.getAttribute('pattern');

        let isValid = true;
        let errorMessage = '';

        if (isRequired && !value) {
            isValid = false;
            errorMessage = 'Este campo es obligatorio';
        } else if (minLength && value.length < parseInt(minLength)) {
            isValid = false;
            errorMessage = `Mínimo ${minLength} caracteres requeridos`;
        } else if (maxLength && value.length > parseInt(maxLength)) {
            isValid = false;
            errorMessage = `Máximo ${maxLength} caracteres permitidos`;
        } else if (pattern && !new RegExp(pattern).test(value)) {
            isValid = false;
            errorMessage = 'Formato inválido';
        }

        this.setInputError(input, isValid, errorMessage);
        return isValid;
    }

    /**
     * Set input error state
     */
    setInputError(input, isValid, errorMessage) {
        const container = input.closest('div');
        let errorElement = container.querySelector('.error-message');

        if (isValid) {
            input.classList.remove('error');
            input.classList.add('success');
            input.setAttribute('aria-invalid', 'false');
            if (errorElement) {
                errorElement.remove();
            }
        } else {
            input.classList.remove('success');
            input.classList.add('error');
            input.setAttribute('aria-invalid', 'true');
            
            if (!errorElement) {
                errorElement = document.createElement('div');
                errorElement.className = 'error-message';
                errorElement.setAttribute('role', 'alert');
                errorElement.setAttribute('aria-live', 'polite');
                container.appendChild(errorElement);
            }
            errorElement.textContent = errorMessage;
        }
    }

    /**
     * Clear input error
     */
    clearInputError(input) {
        const container = input.closest('div');
        const errorElement = container.querySelector('.error-message');
        
        if (errorElement) {
            errorElement.remove();
        }
        
        input.classList.remove('error');
        input.setAttribute('aria-invalid', 'false');
    }
}

// Initialize accessibility manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.accessibilityManager = new AccessibilityManager();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AccessibilityManager;
}
