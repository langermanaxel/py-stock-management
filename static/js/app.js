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

// Variables globales
let purchaseItems = [];
let currentTab = 'dashboard';

// Inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Función de inicialización principal
function initializeApp() {
    loadTabData();
    setupEventListeners();
    updateDashboard();
}

// Configuración de event listeners
function setupEventListeners() {
    // Navegación móvil
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }
    
    // Cerrar menú móvil al hacer click en un enlace
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            if (navMenu) {
                navMenu.classList.remove('active');
            }
        });
    });
    
    // Búsqueda de productos
    const productSearch = document.getElementById('productSearch');
    if (productSearch) {
        productSearch.addEventListener('input', filterProducts);
    }
    
    // Filtro de categorías
    const categoryFilter = document.getElementById('categoryFilter');
    if (categoryFilter) {
        categoryFilter.addEventListener('change', filterProducts);
    }
}

// Navegación entre tabs
function showTab(tabName) {
    // Ocultar todos los tabs
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(tab => tab.classList.remove('active'));
    
    // Remover clase active de todos los enlaces
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => link.classList.remove('active'));
    
    // Mostrar tab seleccionado
    const selectedTab = document.getElementById(tabName);
    if (selectedTab) {
        selectedTab.classList.add('active');
        currentTab = tabName;
    }
    
    // Marcar enlace como activo
    const activeLink = document.querySelector(`[onclick="showTab('${tabName}')"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    }
    
    // Cargar datos del tab
    loadTabData();
}

// Cargar datos según el tab activo
function loadTabData() {
    switch (currentTab) {
        case 'dashboard':
            updateDashboard();
            break;
        case 'categories':
            loadCategories();
            break;
        case 'products':
            loadProducts();
            loadCategoriesForProducts();
            break;
        case 'stock':
            loadStock();
            loadProductsForStock();
            break;
        case 'orders':
            loadPurchaseOrders();
            loadProductsForOrders();
            break;
        case 'purchases':
            loadCompletedPurchases();
            break;
    }
}

// Dashboard
function updateDashboard() {
    Promise.all([
        fetch('/api/products/').then(res => res.json()),
        fetch('/api/stock/').then(res => res.json()),
        fetch('/api/orders/').then(res => res.json()),
        fetch('/api/purchases/').then(res => res.json())
    ]).then(([products, stock, orders, purchases]) => {
        document.getElementById('totalProducts').textContent = products.products?.length || 0;
        document.getElementById('lowStockCount').textContent = stock.low_stock_count || 0;
        document.getElementById('pendingOrders').textContent = orders.pending_count || 0;
        document.getElementById('pendingPurchases').textContent = purchases.pending_count || 0;
    }).catch(error => {
        console.error('Error cargando dashboard:', error);
        showToast('error', 'Error', 'No se pudo cargar el dashboard');
    });
}

// Categorías
function loadCategories() {
    fetch('/api/categories/')
        .then(response => response.json())
        .then(data => {
            const categoriesList = document.getElementById('categoriesList');
            if (data.categories && data.categories.length > 0) {
                categoriesList.innerHTML = data.categories.map(category => `
                    <div class="list-item">
                        <div class="list-item-header">
                            <div class="list-item-title">${category.name}</div>
                            <div class="list-item-actions">
                                <button class="btn btn-secondary btn-sm" onclick="editCategory(${category.id})">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button class="btn btn-danger btn-sm" onclick="deleteCategory(${category.id})">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </div>
                        </div>
                        ${category.description ? `<p class="text-muted">${category.description}</p>` : ''}
                    </div>
                `).join('');
            } else {
                categoriesList.innerHTML = '<p class="text-muted text-center">No hay categorías creadas</p>';
            }
        })
        .catch(error => {
            console.error('Error cargando categorías:', error);
            showToast('error', 'Error', 'No se pudieron cargar las categorías');
        });
}

// Productos
function loadProducts() {
    fetch('/api/products/')
        .then(response => response.json())
        .then(data => {
            const productsList = document.getElementById('productsList');
            if (data.products && data.products.length > 0) {
                productsList.innerHTML = data.products.map(product => `
                    <div class="list-item">
                        <div class="list-item-header">
                            <div class="list-item-title">${product.name}</div>
                            <div class="list-item-actions">
                                <button class="btn btn-secondary btn-sm" onclick="editProduct(${product.id})">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button class="btn btn-danger btn-sm" onclick="deleteProduct(${product.id})">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </div>
                        </div>
                        <p class="text-muted">${product.description}</p>
                        <div class="product-details">
                            <span class="badge badge-primary">$${product.price}</span>
                            <span class="badge badge-secondary">${product.category?.name || 'Sin categoría'}</span>
                        </div>
                    </div>
                `).join('');
            } else {
                productsList.innerHTML = '<p class="text-muted text-center">No hay productos creados</p>';
            }
        })
        .catch(error => {
            console.error('Error cargando productos:', error);
            showToast('error', 'Error', 'No se pudieron cargar los productos');
        });
}

// Stock
function loadStock() {
    fetch('/api/stock/')
        .then(response => response.json())
        .then(data => {
            const stockList = document.getElementById('stockList');
            if (data.stock_items && data.stock_items.length > 0) {
                stockList.innerHTML = data.stock_items.map(item => `
                    <div class="list-item ${item.quantity <= item.min_stock ? 'low-stock' : ''}">
                        <div class="list-item-header">
                            <div class="list-item-title">${item.product?.name || 'Producto no encontrado'}</div>
                            <div class="list-item-actions">
                                <button class="btn btn-secondary btn-sm" onclick="editStock(${item.id})">
                                    <i class="fas fa-edit"></i>
                                </button>
                            </div>
                        </div>
                        <div class="stock-details">
                            <span class="badge badge-info">Stock: ${item.quantity}</span>
                            <span class="badge badge-warning">Mínimo: ${item.min_stock}</span>
                            ${item.quantity <= item.min_stock ? '<span class="badge badge-danger">Stock Bajo</span>' : ''}
                        </div>
                    </div>
                `).join('');
            } else {
                stockList.innerHTML = '<p class="text-muted text-center">No hay registros de stock</p>';
            }
        })
        .catch(error => {
            console.error('Error cargando stock:', error);
            showToast('error', 'Error', 'No se pudo cargar el stock');
        });
}

// Órdenes de compra
function loadPurchaseOrders() {
    fetch('/api/purchases/')
        .then(response => response.json())
        .then(data => {
            const ordersList = document.getElementById('ordersList');
            const pendingOrders = data.purchase_orders?.filter(po => po.status === 'pending') || [];
            
            if (pendingOrders.length > 0) {
                ordersList.innerHTML = pendingOrders.map(order => `
                    <div class="list-item">
                        <div class="list-item-header">
                            <div class="list-item-title">${order.supplier_name}</div>
                            <div class="list-item-actions">
                                <button class="btn btn-success btn-sm" onclick="completePurchaseOrder(${order.id})">
                                    <i class="fas fa-check"></i> Completar
                                </button>
                                <button class="btn btn-danger btn-sm" onclick="deletePurchaseOrder(${order.id})">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </div>
                        </div>
                        <p class="text-muted">Total: $${order.total}</p>
                        <div class="order-items">
                            ${order.items?.map(item => `
                                <span class="badge badge-secondary">
                                    ${item.product?.name || 'Producto no encontrado'} x${item.quantity}
                                </span>
                            `).join('') || ''}
                        </div>
                    </div>
                `).join('');
            } else {
                ordersList.innerHTML = '<p class="text-muted text-center">No hay órdenes pendientes</p>';
            }
        })
        .catch(error => {
            console.error('Error cargando órdenes:', error);
            showToast('error', 'Error', 'No se pudieron cargar las órdenes');
        });
}

// Compras completadas
function loadCompletedPurchases() {
    fetch('/api/purchases/')
        .then(response => response.json())
        .then(data => {
            const purchasesList = document.getElementById('purchasesList');
            const completedPurchases = data.purchase_orders?.filter(po => po.status === 'completed') || [];
            
            if (completedPurchases.length > 0) {
                purchasesList.innerHTML = completedPurchases.map(purchase => `
                    <div class="list-item">
                        <div class="list-item-header">
                            <div class="list-item-title">${purchase.supplier_name}</div>
                            <span class="badge badge-success">Completada</span>
                        </div>
                        <p class="text-muted">Total: $${purchase.total}</p>
                        <p class="text-muted">Completada: ${new Date(purchase.updated_at).toLocaleDateString()}</p>
                        <div class="purchase-items">
                            ${purchase.items?.map(item => `
                                <span class="badge badge-secondary">
                                    ${item.product?.name || 'Producto no encontrado'} x${item.quantity}
                                </span>
                            `).join('') || ''}
                        </div>
                    </div>
                `).join('');
            } else {
                purchasesList.innerHTML = '<p class="text-muted text-center">No hay compras completadas</p>';
            }
        })
        .catch(error => {
            console.error('Error cargando compras:', error);
            showToast('error', 'Error', 'No se pudieron cargar las compras');
        });
}

// Cargar datos para formularios
function loadCategoriesForProducts() {
    fetch('/api/categories/')
        .then(response => response.json())
        .then(data => {
            const categorySelect = document.getElementById('productCategory');
            if (categorySelect && data.categories) {
                categorySelect.innerHTML = '<option value="">Seleccionar categoría</option>' +
                    data.categories.map(cat => `<option value="${cat.id}">${cat.name}</option>`).join('');
            }
        })
        .catch(error => console.error('Error cargando categorías:', error));
}

function loadProductsForStock() {
    fetch('/api/products/')
        .then(response => response.json())
        .then(data => {
            const productSelect = document.getElementById('stockProduct');
            if (productSelect && data.products) {
                productSelect.innerHTML = '<option value="">Seleccionar producto</option>' +
                    data.products.map(prod => `<option value="${prod.id}">${prod.name}</option>`).join('');
            }
        })
        .catch(error => console.error('Error cargando productos:', error));
}

function loadProductsForOrders() {
    fetch('/api/products/')
        .then(response => response.json())
        .then(data => {
            const productSelect = document.getElementById('productSelect');
            if (productSelect && data.products) {
                productSelect.innerHTML = '<option value="">Seleccionar producto</option>' +
                    data.products.map(prod => `<option value="${prod.id}">${prod.name}</option>`).join('');
            }
        })
        .catch(error => console.error('Error cargando productos:', error));
}

// Funciones de formularios
function submitCategory(event) {
    event.preventDefault();
    
    if (!this.validateForm()) {
        showToast('error', 'Error de Validación', 'Por favor corrige los errores en el formulario');
        return;
    }
    
    const formData = new FormData(event.target);
    const categoryData = {
        name: formData.get('name'),
        description: formData.get('description')
    };
    
    fetch('/api/categories/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(categoryData)
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Error al crear categoría');
    })
    .then(data => {
        showToast('success', 'Éxito', 'Categoría creada correctamente');
        this.resetForm();
        loadCategories();
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('error', 'Error', 'No se pudo crear la categoría');
    });
}

function submitProduct(event) {
    event.preventDefault();
    
    if (!this.validateForm()) {
        showToast('error', 'Error de Validación', 'Por favor corrige los errores en el formulario');
        return;
    }
    
    const formData = new FormData(event.target);
    const productData = {
        name: formData.get('name'),
        description: formData.get('description'),
        price: parseFloat(formData.get('price')),
        category_id: parseInt(formData.get('category_id'))
    };
    
    fetch('/api/products/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(productData)
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Error al crear producto');
    })
    .then(data => {
        showToast('success', 'Éxito', 'Producto creado correctamente');
        this.resetForm();
        loadProducts();
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('error', 'Error', 'No se pudo crear el producto');
    });
}

function submitStock(event) {
    event.preventDefault();
    
    if (!this.validateForm()) {
        showToast('error', 'Error de Validación', 'Por favor corrige los errores en el formulario');
        return;
    }
    
    const formData = new FormData(event.target);
    const stockData = {
        product_id: parseInt(formData.get('product_id')),
        quantity: parseInt(formData.get('quantity')),
        min_stock: parseInt(formData.get('min_stock') || 0)
    };
    
    fetch('/api/stock/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(stockData)
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Error al crear stock');
    })
    .then(data => {
        showToast('success', 'Éxito', 'Stock creado correctamente');
        this.resetForm();
        loadStock();
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('error', 'Error', 'No se pudo crear el stock');
    });
}

function submitPurchaseOrder(event) {
    event.preventDefault();
    
    if (!this.validateForm()) {
        showToast('error', 'Error de Validación', 'Por favor corrige los errores en el formulario');
        return;
    }
    
    if (purchaseItems.length === 0) {
        showToast('error', 'Error', 'Debes agregar al menos un producto a la orden');
        return;
    }
    
    const formData = new FormData(event.target);
    const orderData = {
        supplier_name: formData.get('supplier_name'),
        items: purchaseItems
    };
    
    fetch('/api/purchases/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(orderData)
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Error al crear orden de compra');
    })
    .then(data => {
        showToast('success', 'Éxito', 'Orden de compra creada correctamente');
        this.resetForm();
        purchaseItems = [];
        updatePurchaseItems();
        loadPurchaseOrders();
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('error', 'Error', 'No se pudo crear la orden de compra');
    });
}

// Funciones de órdenes de compra
function addPurchaseItem() {
    const productSelect = document.getElementById('productSelect');
    const quantityInput = document.getElementById('quantityInput');
    const unitPriceInput = document.getElementById('unitPriceInput');
    
    if (!productSelect.value || !quantityInput.value || !unitPriceInput.value) {
        showToast('error', 'Error', 'Completa todos los campos del producto');
        return;
    }
    
    const productId = parseInt(productSelect.value);
    const quantity = parseInt(quantityInput.value);
    const unitPrice = parseFloat(unitPriceInput.value);
    
    if (quantity <= 0 || unitPrice < 0) {
        showToast('error', 'Error', 'Cantidad y precio deben ser positivos');
        return;
    }
    
    // Verificar que el producto no esté ya agregado
    const existingItem = purchaseItems.find(item => item.product_id === productId);
    if (existingItem) {
        showToast('warning', 'Advertencia', 'Este producto ya está en la orden');
        return;
    }
    
    purchaseItems.push({
        product_id: productId,
        quantity: quantity,
        unit_price: unitPrice
    });
    
    // Limpiar campos
    productSelect.value = '';
    quantityInput.value = '';
    unitPriceInput.value = '';
    
    updatePurchaseItems();
    updateCreateOrderButton();
}

function updatePurchaseItems() {
    const purchaseItemsDiv = document.getElementById('purchaseItems');
    
    if (purchaseItems.length === 0) {
        purchaseItemsDiv.innerHTML = '<p class="text-muted text-center">No hay productos agregados</p>';
        return;
    }
    
    purchaseItemsDiv.innerHTML = purchaseItems.map((item, index) => `
        <div class="purchase-item">
            <div class="purchase-item-info">
                <strong>Producto ID: ${item.product_id}</strong> - 
                Cantidad: ${item.quantity} - 
                Precio: $${item.unit_price}
            </div>
            <div class="purchase-item-actions">
                <button class="btn btn-danger btn-sm" onclick="removePurchaseItem(${index})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
}

function removePurchaseItem(index) {
    purchaseItems.splice(index, 1);
    updatePurchaseItems();
    updateCreateOrderButton();
}

function updateCreateOrderButton() {
    const createOrderBtn = document.getElementById('createOrderBtn');
    if (createOrderBtn) {
        createOrderBtn.disabled = purchaseItems.length === 0;
    }
}

// Funciones de acciones
function completePurchaseOrder(orderId) {
    if (confirm('¿Estás seguro de que quieres completar esta orden de compra?')) {
        fetch(`/api/purchases/${orderId}/complete`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Error al completar orden');
        })
        .then(data => {
            showToast('success', 'Éxito', 'Orden de compra completada correctamente');
            loadPurchaseOrders();
            loadCompletedPurchases();
            updateDashboard();
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('error', 'Error', 'No se pudo completar la orden');
        });
    }
}

function deletePurchaseOrder(orderId) {
    if (confirm('¿Estás seguro de que quieres eliminar esta orden de compra?')) {
        fetch(`/api/purchases/${orderId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                showToast('success', 'Éxito', 'Orden de compra eliminada correctamente');
                loadPurchaseOrders();
                updateDashboard();
            } else {
                throw new Error('Error al eliminar orden');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('error', 'Error', 'No se pudo eliminar la orden');
        });
    }
}

// Funciones de edición (placeholders)
function editCategory(id) {
    showToast('info', 'Función en desarrollo', 'La edición de categorías estará disponible próximamente');
}

function editProduct(id) {
    showToast('info', 'Función en desarrollo', 'La edición de productos estará disponible próximamente');
}

function editStock(id) {
    showToast('info', 'Función en desarrollo', 'La edición de stock estará disponible próximamente');
}

function deleteCategory(id) {
    if (confirm('¿Estás seguro de que quieres eliminar esta categoría?')) {
        fetch(`/api/categories/${id}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                showToast('success', 'Éxito', 'Categoría eliminada correctamente');
                loadCategories();
            } else {
                throw new Error('Error al eliminar categoría');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('error', 'Error', 'No se pudo eliminar la categoría');
        });
    }
}

function deleteProduct(id) {
    if (confirm('¿Estás seguro de que quieres eliminar este producto?')) {
        fetch(`/api/products/${id}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                showToast('success', 'Éxito', 'Producto eliminado correctamente');
                loadProducts();
            } else {
                throw new Error('Error al eliminar producto');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('error', 'Error', 'No se pudo eliminar el producto');
        });
    }
}

// Filtros y búsqueda
function filterProducts() {
    const searchTerm = document.getElementById('productSearch')?.value.toLowerCase() || '';
    const categoryFilter = document.getElementById('categoryFilter')?.value || '';
    
    // Implementar lógica de filtrado
    // Por ahora solo recargamos los productos
    loadProducts();
}

// Navegación móvil
function toggleNav() {
    const navMenu = document.querySelector('.nav-menu');
    if (navMenu) {
        navMenu.classList.toggle('active');
    }
}

// Función helper para mostrar toasts (fallback si Alpine.js no está disponible)
function showToast(type, title, message, duration = 5000) {
    // Intentar usar Alpine.js si está disponible
    if (window.Alpine && window.Alpine.store && window.Alpine.store('toast')) {
        window.Alpine.store('toast').showToast(type, title, message, duration);
        return;
    }
    
    // Fallback: alert simple
    alert(`${title}: ${message}`);
}

// Exportar funciones para uso global
window.showTab = showTab;
window.addPurchaseItem = addPurchaseItem;
window.removePurchaseItem = removePurchaseItem;
window.completePurchaseOrder = completePurchaseOrder;
window.deletePurchaseOrder = deletePurchaseOrder;
window.editCategory = editCategory;
window.editProduct = editProduct;
window.editStock = editStock;
window.deleteCategory = deleteCategory;
window.deleteProduct = deleteProduct;
window.toggleNav = toggleNav;
window.showToast = showToast; 