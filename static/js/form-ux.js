/**
 * Form UX and validation management
 */

class FormUXManager {
    constructor() {
        this.submittedForms = new Set();
        this.init();
    }

    init() {
        this.setupFormValidation();
        this.setupKeyboardShortcuts();
        this.setupDoubleSubmitPrevention();
    }

    /**
     * Setup form validation for all forms
     */
    setupFormValidation() {
        document.addEventListener('DOMContentLoaded', () => {
            const forms = document.querySelectorAll('form');
            forms.forEach(form => {
                this.enhanceForm(form);
            });
        });
    }

    /**
     * Enhance a form with validation and UX improvements
     */
    enhanceForm(form) {
        // Add form ID if it doesn't have one
        if (!form.id) {
            form.id = `form-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        }

        // Setup input validation
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            this.setupInputValidation(input);
        });

        // Setup form submission
        form.addEventListener('submit', (e) => {
            this.handleFormSubmit(e, form);
        });

        // Setup real-time validation
        form.addEventListener('input', (e) => {
            if (e.target.matches('input, select, textarea')) {
                this.validateInput(e.target);
            }
        });

        // Setup blur validation
        form.addEventListener('blur', (e) => {
            if (e.target.matches('input, select, textarea')) {
                this.validateInput(e.target, true);
            }
        }, true);
    }

    /**
     * Setup input validation
     */
    setupInputValidation(input) {
        // Add required indicator
        if (input.hasAttribute('required')) {
            const label = document.querySelector(`label[for="${input.id}"]`);
            if (label && !label.querySelector('.required-indicator')) {
                const indicator = document.createElement('span');
                indicator.className = 'required-indicator text-red-500 ml-1';
                indicator.textContent = '*';
                indicator.setAttribute('aria-label', 'Campo obligatorio');
                label.appendChild(indicator);
            }
        }

        // Setup number input validation
        if (input.type === 'number') {
            input.addEventListener('input', () => {
                this.validateNumberInput(input);
            });
        }

        // Setup email validation
        if (input.type === 'email') {
            input.addEventListener('input', () => {
                this.validateEmailInput(input);
            });
        }

        // Setup password validation
        if (input.type === 'password') {
            input.addEventListener('input', () => {
                this.validatePasswordInput(input);
            });
        }
    }

    /**
     * Validate individual input
     */
    validateInput(input, showErrors = false) {
        const value = input.value.trim();
        const isRequired = input.hasAttribute('required');
        const errors = [];

        // Required validation
        if (isRequired && !value) {
            errors.push('Este campo es obligatorio');
        }

        // Type-specific validation
        if (value) {
            switch (input.type) {
                case 'email':
                    if (!this.isValidEmail(value)) {
                        errors.push('Ingresa un email válido');
                    }
                    break;
                case 'number':
                    if (!this.isValidNumber(input)) {
                        errors.push('Ingresa un número válido');
                    }
                    break;
                case 'password':
                    if (!this.isValidPassword(value)) {
                        errors.push('La contraseña debe tener al menos 6 caracteres');
                    }
                    break;
            }

            // Min/Max length validation
            const minLength = input.getAttribute('minlength');
            const maxLength = input.getAttribute('maxlength');
            
            if (minLength && value.length < parseInt(minLength)) {
                errors.push(`Mínimo ${minLength} caracteres requeridos`);
            }
            
            if (maxLength && value.length > parseInt(maxLength)) {
                errors.push(`Máximo ${maxLength} caracteres permitidos`);
            }

            // Pattern validation
            const pattern = input.getAttribute('pattern');
            if (pattern && !new RegExp(pattern).test(value)) {
                errors.push('Formato inválido');
            }
        }

        // Show/hide errors
        this.setInputErrors(input, errors, showErrors);
        
        return errors.length === 0;
    }

    /**
     * Validate number input
     */
    validateNumberInput(input) {
        const value = input.value;
        const min = parseFloat(input.getAttribute('min'));
        const max = parseFloat(input.getAttribute('max'));
        const step = parseFloat(input.getAttribute('step')) || 1;

        if (value && !isNaN(value)) {
            const numValue = parseFloat(value);
            
            if (min !== null && numValue < min) {
                this.setInputErrors(input, [`El valor mínimo es ${min}`], true);
                return false;
            }
            
            if (max !== null && numValue > max) {
                this.setInputErrors(input, [`El valor máximo es ${max}`], true);
                return false;
            }

            // Check step
            if (step && (numValue % step) !== 0) {
                this.setInputErrors(input, [`El valor debe ser múltiplo de ${step}`], true);
                return false;
            }
        }

        this.setInputErrors(input, [], true);
        return true;
    }

    /**
     * Validate email input
     */
    validateEmailInput(input) {
        const value = input.value.trim();
        if (value && !this.isValidEmail(value)) {
            this.setInputErrors(input, ['Ingresa un email válido'], true);
            return false;
        }
        this.setInputErrors(input, [], true);
        return true;
    }

    /**
     * Validate password input
     */
    validatePasswordInput(input) {
        const value = input.value;
        if (value && !this.isValidPassword(value)) {
            this.setInputErrors(input, ['La contraseña debe tener al menos 6 caracteres'], true);
            return false;
        }
        this.setInputErrors(input, [], true);
        return true;
    }

    /**
     * Set input errors
     */
    setInputErrors(input, errors, showErrors = false) {
        const container = input.closest('.form-group') || input.closest('div');
        let errorContainer = container.querySelector('.error-messages');

        if (errors.length > 0 && showErrors) {
            if (!errorContainer) {
                errorContainer = document.createElement('div');
                errorContainer.className = 'error-messages mt-1';
                container.appendChild(errorContainer);
            }

            errorContainer.innerHTML = errors.map(error => 
                `<div class="error-message" role="alert" aria-live="polite">${error}</div>`
            ).join('');

            input.classList.add('error');
            input.setAttribute('aria-invalid', 'true');
        } else {
            if (errorContainer) {
                errorContainer.remove();
            }
            input.classList.remove('error');
            input.setAttribute('aria-invalid', 'false');
        }
    }

    /**
     * Handle form submission
     */
    handleFormSubmit(e, form) {
        e.preventDefault();

        // Prevent double submit
        if (this.submittedForms.has(form.id)) {
            return;
        }

        // Validate all inputs
        const inputs = form.querySelectorAll('input, select, textarea');
        let isValid = true;

        inputs.forEach(input => {
            if (!this.validateInput(input, true)) {
                isValid = false;
            }
        });

        if (!isValid) {
            // Focus first invalid input
            const firstInvalid = form.querySelector('.error');
            if (firstInvalid) {
                firstInvalid.focus();
            }
            return;
        }

        // Mark form as submitted
        this.submittedForms.add(form.id);

        // Disable submit button
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            this.setButtonLoading(submitButton, true);
        }

        // Submit form
        this.submitForm(form);
    }

    /**
     * Submit form with proper handling
     */
    async submitForm(form) {
        try {
            const formData = new FormData(form);
            const action = form.action || window.location.href;
            const method = form.method || 'POST';

            const response = await fetch(action, {
                method: method,
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.ok) {
                const result = await response.json();
                this.handleSubmitSuccess(form, result);
            } else {
                const error = await response.json();
                this.handleSubmitError(form, error);
            }
        } catch (error) {
            this.handleSubmitError(form, { message: 'Error de conexión' });
        } finally {
            // Re-enable form
            this.submittedForms.delete(form.id);
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                this.setButtonLoading(submitButton, false);
            }
        }
    }

    /**
     * Handle successful form submission
     */
    handleSubmitSuccess(form, result) {
        // Show success message
        if (window.feedbackManager) {
            window.feedbackManager.success('Éxito', result.message || 'Formulario enviado correctamente');
        }

        // Reset form if needed
        if (result.resetForm !== false) {
            form.reset();
            this.clearFormErrors(form);
        }

        // Close modal if in modal
        const modal = form.closest('[role="dialog"]');
        if (modal) {
            this.closeModal(modal);
        }

        // Redirect if specified
        if (result.redirect) {
            window.location.href = result.redirect;
        }
    }

    /**
     * Handle form submission error
     */
    handleSubmitError(form, error) {
        // Show error message
        if (window.feedbackManager) {
            window.feedbackManager.error('Error', error.message || 'Ocurrió un error al enviar el formulario');
        }

        // Show field-specific errors
        if (error.errors) {
            Object.keys(error.errors).forEach(fieldName => {
                const input = form.querySelector(`[name="${fieldName}"]`);
                if (input) {
                    this.setInputErrors(input, [error.errors[fieldName]], true);
                }
            });
        }
    }

    /**
     * Clear all form errors
     */
    clearFormErrors(form) {
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            this.setInputErrors(input, [], false);
        });
    }

    /**
     * Set button loading state
     */
    setButtonLoading(button, loading = true) {
        if (loading) {
            button.classList.add('btn-loading');
            button.disabled = true;
            button.setAttribute('aria-busy', 'true');
        } else {
            button.classList.remove('btn-loading');
            button.disabled = false;
            button.removeAttribute('aria-busy');
        }
    }

    /**
     * Setup keyboard shortcuts
     */
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Enter to submit form
            if (e.key === 'Enter' && !e.shiftKey && !e.ctrlKey && !e.altKey) {
                const activeElement = document.activeElement;
                if (activeElement && activeElement.form) {
                    const form = activeElement.form;
                    const submitButton = form.querySelector('button[type="submit"]');
                    if (submitButton && !submitButton.disabled) {
                        e.preventDefault();
                        submitButton.click();
                    }
                }
            }

            // Escape to close modal
            if (e.key === 'Escape') {
                const modal = document.querySelector('[role="dialog"]:not([style*="display: none"])');
                if (modal) {
                    this.closeModal(modal);
                }
            }
        });
    }

    /**
     * Close modal
     */
    closeModal(modal) {
        // Trigger close event
        const closeEvent = new CustomEvent('close-modal');
        modal.dispatchEvent(closeEvent);

        // Hide modal
        modal.style.display = 'none';
        modal.classList.add('hidden');
    }

    /**
     * Setup double submit prevention
     */
    setupDoubleSubmitPrevention() {
        // Add unique token to forms
        document.addEventListener('DOMContentLoaded', () => {
            const forms = document.querySelectorAll('form');
            forms.forEach(form => {
                if (!form.querySelector('input[name="form_token"]')) {
                    const token = this.generateFormToken();
                    const tokenInput = document.createElement('input');
                    tokenInput.type = 'hidden';
                    tokenInput.name = 'form_token';
                    tokenInput.value = token;
                    form.appendChild(tokenInput);
                }
            });
        });
    }

    /**
     * Generate unique form token
     */
    generateFormToken() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }

    /**
     * Validation helper methods
     */
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    isValidNumber(input) {
        const value = input.value;
        if (!value) return true;
        
        const num = parseFloat(value);
        return !isNaN(num) && isFinite(num);
    }

    isValidPassword(password) {
        return password.length >= 6;
    }

    /**
     * Public API methods
     */
    
    /**
     * Validate form manually
     */
    validateForm(form) {
        const inputs = form.querySelectorAll('input, select, textarea');
        let isValid = true;

        inputs.forEach(input => {
            if (!this.validateInput(input, true)) {
                isValid = false;
            }
        });

        return isValid;
    }

    /**
     * Reset form
     */
    resetForm(form) {
        form.reset();
        this.clearFormErrors(form);
        this.submittedForms.delete(form.id);
    }

    /**
     * Enable/disable form
     */
    setFormEnabled(form, enabled = true) {
        const inputs = form.querySelectorAll('input, select, textarea, button');
        inputs.forEach(input => {
            input.disabled = !enabled;
        });
    }
}

// Initialize form UX manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.formUXManager = new FormUXManager();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FormUXManager;
}
