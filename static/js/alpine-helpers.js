// ========================================
// ALPINE.JS HELPERS - FUNCIONES AUXILIARES
// ========================================

// Sistema de Notificaciones Toast con Alpine.js
function toastManager() {
    return {
        toasts: [],
        nextId: 1,
        
        showToast(type, title, message, duration = 5000) {
            const toast = {
                id: this.nextId++,
                type,
                title,
                message,
                visible: true,
                timestamp: Date.now()
            };
            
            this.toasts.push(toast);
            
            // Auto-remove después del tiempo especificado
            setTimeout(() => {
                this.removeToast(toast.id);
            }, duration);
            
            return toast.id;
        },
        
        removeToast(id) {
            const index = this.toasts.findIndex(t => t.id === id);
            if (index > -1) {
                this.toasts.splice(index, 1);
            }
        },
        
        getToastIcon(type) {
            const icons = {
                success: 'fas fa-check-circle',
                error: 'fas fa-exclamation-circle',
                warning: 'fas fa-exclamation-triangle',
                info: 'fas fa-info-circle'
            };
            return icons[type] || icons.info;
        },
        
        // Métodos de conveniencia
        success(title, message, duration) {
            return this.showToast('success', title, message, duration);
        },
        
        error(title, message, duration) {
            return this.showToast('error', title, message, duration);
        },
        
        warning(title, message, duration) {
            return this.showToast('warning', title, message, duration);
        },
        
        info(title, message, duration) {
            return this.showToast('info', title, message, duration);
        }
    };
}

// Validador de Formularios con Alpine.js
function formValidator() {
    return {
        formData: {},
        errors: {},
        
        validateField(fieldName) {
            const field = this.$el.querySelector(`[name="${fieldName}"]`);
            if (!field) return;
            
            const value = field.value;
            const rules = this.getFieldRules(fieldName);
            
            // Limpiar error previo
            this.errors[fieldName] = null;
            
            // Aplicar validaciones
            for (const rule of rules) {
                const result = this.validateRule(value, rule);
                if (result !== true) {
                    this.errors[fieldName] = result;
                    break;
                }
            }
            
            // Actualizar clases CSS
            this.updateFieldClasses(field, fieldName);
        },
        
        getFieldRules(fieldName) {
            const rules = [];
            const field = this.$el.querySelector(`[name="${fieldName}"]`);
            
            if (!field) return rules;
            
            // Reglas basadas en atributos HTML5
            if (field.required) {
                rules.push({ type: 'required', message: 'Este campo es requerido' });
            }
            
            if (field.minLength) {
                rules.push({ 
                    type: 'minLength', 
                    value: field.minLength, 
                    message: `Mínimo ${field.minLength} caracteres` 
                });
            }
            
            if (field.maxLength) {
                rules.push({ 
                    type: 'maxLength', 
                    value: field.maxLength, 
                    message: `Máximo ${field.maxLength} caracteres` 
                });
            }
            
            if (field.min) {
                rules.push({ 
                    type: 'min', 
                    value: parseFloat(field.min), 
                    message: `Valor mínimo: ${field.min}` 
                });
            }
            
            if (field.step) {
                rules.push({ 
                    type: 'step', 
                    value: parseFloat(field.step), 
                    message: `Incremento: ${field.step}` 
                });
            }
            
            // Reglas específicas por campo
            if (fieldName === 'email') {
                rules.push({ 
                    type: 'email', 
                    message: 'Formato de email inválido' 
                });
            }
            
            if (fieldName === 'price' || fieldName === 'unit_price') {
                rules.push({ 
                    type: 'positive', 
                    message: 'El precio debe ser positivo' 
                });
            }
            
            if (fieldName === 'quantity') {
                rules.push({ 
                    type: 'positive', 
                    message: 'La cantidad debe ser positiva' 
                });
            }
            
            return rules;
        },
        
        validateRule(value, rule) {
            switch (rule.type) {
                case 'required':
                    return value.trim() !== '' ? true : rule.message;
                    
                case 'minLength':
                    return value.length >= rule.value ? true : rule.message;
                    
                case 'maxLength':
                    return value.length <= rule.value ? true : rule.message;
                    
                case 'min':
                    return parseFloat(value) >= rule.value ? true : rule.message;
                    
                case 'step':
                    const num = parseFloat(value);
                    const step = rule.value;
                    return (num % step) === 0 ? true : rule.message;
                    
                case 'email':
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    return emailRegex.test(value) ? true : rule.message;
                    
                case 'positive':
                    return parseFloat(value) > 0 ? true : rule.message;
                    
                default:
                    return true;
            }
        },
        
        updateFieldClasses(field, fieldName) {
            field.classList.remove('success', 'error');
            
            if (this.errors[fieldName]) {
                field.classList.add('error');
            } else if (field.value.trim() !== '') {
                field.classList.add('success');
            }
        },
        
        validateForm() {
            const fields = this.$el.querySelectorAll('[name]');
            let isValid = true;
            
            fields.forEach(field => {
                this.validateField(field.name);
                if (this.errors[field.name]) {
                    isValid = false;
                }
            });
            
            return isValid;
        },
        
        resetForm() {
            this.formData = {};
            this.errors = {};
            this.$el.reset();
            
            // Limpiar clases CSS
            const fields = this.$el.querySelectorAll('input, select, textarea');
            fields.forEach(field => {
                field.classList.remove('success', 'error');
            });
        }
    };
}

// Exportar funciones para uso global
window.toastManager = toastManager;
window.formValidator = formValidator;
