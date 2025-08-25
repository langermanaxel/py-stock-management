// ========================================
// SISTEMA DE GESTIÓN DE INVENTARIO - APP.JS
// ========================================

// Variables globales
let purchaseItems = [];
let currentTab = 'dashboard';

// Sistema de inicialización robusto
class AppInitializer {
    constructor() {
        this.initialized = false;
        this.initQueue = [];
    }

    // Agregar función a la cola de inicialización
    addToInitQueue(fn) {
        if (this.initialized) {
            fn();
        } else {
            this.initQueue.push(fn);
        }
    }

    // Marcar como inicializado y ejecutar cola
    markAsInitialized() {
        this.initialized = true;
        this.initQueue.forEach(fn => fn());
        this.initQueue = [];
    }

    // Verificar si está inicializado
    isInitialized() {
        return this.initialized;
    }
}

// Instancia global del inicializador
const appInitializer = new AppInitializer();

// Función helper para esperar a que authManager esté listo
async function waitForAuthManager() {
    // Esperar a que authManager esté disponible
    while (!window.authManager || !window.authManager.isAuthenticated()) {
        await new Promise(resolve => setTimeout(resolve, 100));
    }
    
    // Esperar a que se inicialice completamente
    await window.authManager.initialize();
    return true;
}

// ========================================
// INICIALIZACIÓN DE LA APLICACIÓN
// ========================================

// Inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Esperar a que authManager esté listo antes de inicializar
    waitForAuthManager().then(() => {
        initializeApp();
        appInitializer.markAsInitialized();
    }).catch(error => {
        console.error('Error inicializando authManager:', error);
        showToast('error', 'Error', 'No se pudo inicializar la aplicación');
    });
});

// Función de inicialización principal
function initializeApp() {
    loadTabData();
    setupEventListeners();
    updateDashboard();
}

// Configuración de event listeners
function setupEventListeners() {
    const guard = new DOMGuard();
    
    // Solo ejecutar en el dashboard
    guard.executeOnDashboard(() => {
        // Navegación móvil
        guard.safeAddEventListener('.nav-toggle', 'click', () => {
            guard.safeExecute('.nav-menu', (navMenu) => {
                navMenu.classList.toggle('active');
            });
        });
        
        // Cerrar menú móvil al hacer click en un enlace
        guard.safeExecute('.nav-menu', (navMenu) => {
            const navLinks = navMenu.querySelectorAll('.nav-link');
            navLinks.forEach(link => {
                link.addEventListener('click', () => {
                    navMenu.classList.remove('active');
                });
            });
        });
        
        // Búsqueda de productos
        guard.safeAddEventListener('#productSearch', 'input', filterProducts);
        
        // Filtro de categorías
        guard.safeAddEventListener('#categoryFilter', 'change', filterProducts);
    });
}

// ========================================
// NAVEGACIÓN Y TABS
// ========================================

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
    // Esperar a que la app esté inicializada
    appInitializer.addToInitQueue(() => {
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
    });
}

// ========================================
// FUNCIONES DE CARGA DE DATOS
// ========================================

// Dashboard
async function updateDashboard() {
    // Verificar que authManager esté disponible
    if (!window.authManager || !window.authManager.isAuthenticated()) {
        console.warn('AuthManager no disponible, saltando carga del dashboard');
        return;
    }

    try {
        const [productsRes, stockRes, ordersRes, purchasesRes] = await Promise.all([
            authManager.authenticatedRequest('/api/products/'),
            authManager.authenticatedRequest('/api/stock/'),
            authManager.authenticatedRequest('/api/orders/'),
            authManager.authenticatedRequest('/api/purchases/')
        ]);
        
        if (!productsRes || !stockRes || !ordersRes || !purchasesRes) return;
        
        const [products, stock, orders, purchases] = await Promise.all([
            productsRes.json(),
            stockRes.json(),
            ordersRes.json(),
            purchasesRes.json()
        ]);
        
        document.getElementById('totalProducts').textContent = products.products?.length || 0;
        document.getElementById('lowStockCount').textContent = stock.low_stock_count || 0;
        document.getElementById('pendingOrders').textContent = orders.pending_count || 0;
        document.getElementById('pendingPurchases').textContent = purchases.pending_count || 0;
    } catch (error) {
        console.error('Error cargando dashboard:', error);
        showToast('error', 'Error', 'No se pudo cargar el dashboard');
    }
}

// Función para cargar categorías
async function loadCategories() {
    try {
        if (!authManager.isAuthenticated()) {
            console.warn('Usuario no autenticado, saltando carga de categorías');
            return;
        }

        const categories = await authManager.authenticatedRequest('/api/categories');
        if (categories && Array.isArray(categories)) {
            window.categories = categories;
            updateCategoryFilter();
            updateCategoryTable();
        }
    } catch (error) {
        showError(error, 'Error cargando categorías');
    }
}

// Función para cargar productos
async function loadProducts() {
    try {
        if (!authManager.isAuthenticated()) {
            console.warn('Usuario no autenticado, saltando carga de productos');
            return;
        }

        const products = await authManager.authenticatedRequest('/api/products');
        if (products && Array.isArray(products)) {
            window.products = products;
            updateProductTable();
            updateProductSearch();
        }
    } catch (error) {
        showError(error, 'Error cargando productos');
    }
}

// Función para cargar stock
async function loadStock() {
    try {
        if (!authManager.isAuthenticated()) {
            console.warn('Usuario no autenticado, saltando carga de stock');
            return;
        }

        const stock = await authManager.authenticatedRequest('/api/stock');
        if (stock && Array.isArray(stock)) {
            window.stock = stock;
            updateStockTable();
        }
    } catch (error) {
        showError(error, 'Error cargando stock');
    }
}

// Órdenes de compra
async function loadPurchaseOrders() {
    // Verificar que authManager esté disponible
    if (!window.authManager || !window.authManager.isAuthenticated()) {
        console.warn('AuthManager no disponible, saltando carga de órdenes');
        return;
    }

    try {
        const response = await authManager.authenticatedRequest('/api/purchases/');
        if (!response) return;
        
        const data = await response.json();
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
    } catch (error) {
        console.error('Error cargando órdenes:', error);
        showToast('error', 'Error', 'No se pudieron cargar las órdenes');
    }
}

// Compras completadas
async function loadCompletedPurchases() {
    // Verificar que authManager esté disponible
    if (!window.authManager || !window.authManager.isAuthenticated()) {
        console.warn('AuthManager no disponible, saltando carga de compras');
        return;
    }

    try {
        const response = await authManager.authenticatedRequest('/api/purchases/');
        if (!response) return;
        
        const data = await response.json();
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
    } catch (error) {
        console.error('Error cargando compras:', error);
        showToast('error', 'Error', 'No se pudieron cargar las compras');
    }
}

// Cargar datos para formularios
async function loadCategoriesForProducts() {
    // Verificar que authManager esté disponible
    if (!window.authManager || !window.authManager.isAuthenticated()) {
        console.warn('AuthManager no disponible, saltando carga de categorías para productos');
        return;
    }

    try {
        const response = await authManager.authenticatedRequest('/api/categories/');
        if (!response) return;
        
        const data = await response.json();
        const categorySelect = document.getElementById('productCategory');
        if (categorySelect && data.categories) {
            categorySelect.innerHTML = '<option value="">Seleccionar categoría</option>' +
                data.categories.map(cat => `<option value="${cat.id}">${cat.name}</option>`).join('');
        }
    } catch (error) {
        console.error('Error cargando categorías:', error);
    }
}

async function loadProductsForStock() {
    // Verificar que authManager esté disponible
    if (!window.authManager || !window.authManager.isAuthenticated()) {
        console.warn('AuthManager no disponible, saltando carga de productos para stock');
        return;
    }

    try {
        const response = await authManager.authenticatedRequest('/api/products/');
        if (!response) return;
        
        const data = await response.json();
        const productSelect = document.getElementById('stockProduct');
        if (productSelect && data.products) {
            productSelect.innerHTML = '<option value="">Seleccionar producto</option>' +
                data.products.map(prod => `<option value="${prod.id}">${prod.name}</option>`).join('');
        }
    } catch (error) {
        console.error('Error cargando productos:', error);
    }
}

async function loadProductsForOrders() {
    // Verificar que authManager esté disponible
    if (!window.authManager || !window.authManager.isAuthenticated()) {
        console.warn('AuthManager no disponible, saltando carga de productos para órdenes');
        return;
    }

    try {
        const response = await authManager.authenticatedRequest('/api/products/');
        if (!response) return;
        
        const data = await response.json();
        const productSelect = document.getElementById('productSelect');
        if (productSelect && data.products) {
            productSelect.innerHTML = '<option value="">Seleccionar producto</option>' +
                data.products.map(prod => `<option value="${prod.id}">${prod.name}</option>`).join('');
        }
    } catch (error) {
        console.error('Error cargando productos:', error);
    }
}

// ========================================
// FUNCIONES DE FORMULARIOS
// ========================================

// Función para crear categoría
async function submitCategory(event) {
    event.preventDefault();
    
    try {
        const formData = new FormData(event.target);
        const categoryData = {
            name: formData.get('name'),
            description: formData.get('description')
        };

        const response = await authManager.authenticatedRequest('/api/categories', {
            method: 'POST',
            body: JSON.stringify(categoryData)
        });

        showSuccess('Categoría creada exitosamente');
        event.target.reset();
        await loadCategories();
        
        // Cerrar modal si existe
        const modal = document.querySelector('#categoryModal');
        if (modal && window.bootstrap) {
            const bootstrapModal = window.bootstrap.Modal.getInstance(modal);
            if (bootstrapModal) {
                bootstrapModal.hide();
            }
        }
    } catch (error) {
        showError(error, 'Error creando categoría');
    }
}

// Función para crear producto
async function submitProduct(event) {
    event.preventDefault();
    
    try {
        const formData = new FormData(event.target);
        const productData = {
            name: formData.get('name'),
            description: formData.get('description'),
            price: parseFloat(formData.get('price')),
            category_id: parseInt(formData.get('category_id'))
        };

        const response = await authManager.authenticatedRequest('/api/products', {
            method: 'POST',
            body: JSON.stringify(productData)
        });

        showSuccess('Producto creado exitosamente');
        event.target.reset();
        await loadProducts();
        
        // Cerrar modal si existe
        const modal = document.querySelector('#productModal');
        if (modal && window.bootstrap) {
            const bootstrapModal = window.bootstrap.Modal.getInstance(modal);
            if (bootstrapModal) {
                bootstrapModal.hide();
            }
        }
    } catch (error) {
        showError(error, 'Error creando producto');
    }
}

// Función para crear stock
async function submitStock(event) {
    event.preventDefault();
    
    try {
        const formData = new FormData(event.target);
        const stockData = {
            product_id: parseInt(formData.get('product_id')),
            quantity: parseInt(formData.get('quantity')),
            location: formData.get('location')
        };

        const response = await authManager.authenticatedRequest('/api/stock', {
            method: 'POST',
            body: JSON.stringify(stockData)
        });

        showSuccess('Stock creado exitosamente');
        event.target.reset();
        await loadStock();
        
        // Cerrar modal si existe
        const modal = document.querySelector('#stockModal');
        if (modal && window.bootstrap) {
            const bootstrapModal = window.bootstrap.Modal.getInstance(modal);
            if (bootstrapModal) {
                bootstrapModal.hide();
            }
        }
    } catch (error) {
        showError(error, 'Error creando stock');
    }
}

// Órdenes de compra
async function submitPurchaseOrder(event) {
    // Verificar que authManager esté disponible
    if (!window.authManager || !window.authManager.isAuthenticated()) {
        showToast('error', 'Error', 'No estás autenticado');
        return;
    }

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
    
    try {
        const response = await authManager.authenticatedRequest('/api/purchases/', {
            method: 'POST',
            body: JSON.stringify(orderData)
        });
        
        if (response && response.ok) {
            const data = await response.json();
            showToast('success', 'Éxito', 'Orden de compra creada correctamente');
            this.resetForm();
            purchaseItems = [];
            updatePurchaseItems();
            loadPurchaseOrders();
        } else {
            throw new Error('Error al crear orden de compra');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('error', 'Error', 'No se pudo crear la orden de compra');
    }
}

// ========================================
// FUNCIONES DE ÓRDENES DE COMPRA
// ========================================

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

// ========================================
// FUNCIONES DE ACCIONES
// ========================================

async function completePurchaseOrder(orderId) {
    // Verificar que authManager esté disponible
    if (!window.authManager || !window.authManager.isAuthenticated()) {
        showToast('error', 'Error', 'No estás autenticado');
        return;
    }

    if (confirm('¿Estás seguro de que quieres completar esta orden de compra?')) {
        try {
            const response = await authManager.authenticatedRequest(`/api/purchases/${orderId}/complete`, {
                method: 'PUT'
            });
            
            if (response && response.ok) {
                const data = await response.json();
                showToast('success', 'Éxito', 'Orden de compra completada correctamente');
                loadPurchaseOrders();
                loadCompletedPurchases();
                updateDashboard();
            } else {
                throw new Error('Error al completar orden');
            }
        } catch (error) {
            console.error('Error:', error);
            showToast('error', 'Error', 'No se pudo completar la orden');
        }
    }
}

async function deletePurchaseOrder(orderId) {
    // Verificar que authManager esté disponible
    if (!window.authManager || !window.authManager.isAuthenticated()) {
        showToast('error', 'Error', 'No estás autenticado');
        return;
    }

    if (confirm('¿Estás seguro de que quieres eliminar esta orden de compra?')) {
        try {
            const response = await authManager.authenticatedRequest(`/api/purchases/${orderId}`, {
                method: 'DELETE'
            });
            
            if (response && response.ok) {
                showToast('success', 'Éxito', 'Orden de compra eliminada correctamente');
                loadPurchaseOrders();
                updateDashboard();
            } else {
                throw new Error('Error al eliminar orden');
            }
        } catch (error) {
            console.error('Error:', error);
            showToast('error', 'Error', 'No se pudo eliminar la orden');
        }
    }
}

// ========================================
// FUNCIONES DE EDICIÓN (PLACEHOLDERS)
// ========================================

function editCategory(id) {
    if (!checkPermission('edit_category', 'manager')) return;
    showToast('info', 'Función en desarrollo', 'La edición de categorías estará disponible próximamente');
}

function editProduct(id) {
    if (!checkPermission('edit_product', 'manager')) return;
    showToast('info', 'Función en desarrollo', 'La edición de productos estará disponible próximamente');
}

function editStock(id) {
    if (!checkPermission('edit_stock', 'manager')) return;
    showToast('info', 'Función en desarrollo', 'La edición de stock estará disponible próximamente');
}

async function deleteCategory(id) {
    // Verificar que authManager esté disponible
    if (!window.authManager || !window.authManager.isAuthenticated()) {
        showToast('error', 'Error', 'No estás autenticado');
        return;
    }

    if (!checkPermission('delete_category', 'admin')) return;
    
    if (confirm('¿Estás seguro de que quieres eliminar esta categoría?')) {
        try {
            const response = await authManager.authenticatedRequest(`/api/categories/${id}`, {
                method: 'DELETE'
            });
            
            if (response && response.ok) {
                showToast('success', 'Éxito', 'Categoría eliminada correctamente');
                loadCategories();
            } else {
                throw new Error('Error al eliminar categoría');
            }
        } catch (error) {
            console.error('Error:', error);
            showToast('error', 'Error', 'No se pudo eliminar la categoría');
        }
    }
}

async function deleteProduct(id) {
    // Verificar que authManager esté disponible
    if (!window.authManager || !window.authManager.isAuthenticated()) {
        showToast('error', 'Error', 'No estás autenticado');
        return;
    }

    if (!checkPermission('delete_product', 'admin')) return;
    
    if (confirm('¿Estás seguro de que quieres eliminar este producto?')) {
        try {
            const response = await authManager.authenticatedRequest(`/api/products/${id}`, {
                method: 'DELETE'
            });
            
            if (response && response.ok) {
                showToast('success', 'Éxito', 'Producto eliminado correctamente');
                loadProducts();
            } else {
                throw new Error('Error al eliminar producto');
            }
        } catch (error) {
            console.error('Error:', error);
            showToast('error', 'Error', 'No se pudo eliminar el producto');
        }
    }
}

// ========================================
// FUNCIONES AUXILIARES
// ========================================

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

// Función para mostrar errores de manera consistente
function showError(error, title = 'Error') {
    if (window.showError) {
        window.showError(error, title);
    } else {
        console.error(`${title}:`, error);
        alert(`${title}: ${error.message || error}`);
    }
}

// Función para mostrar mensajes de éxito de manera consistente
function showSuccess(message, title = 'Éxito') {
    if (window.showSuccess) {
        window.showSuccess(message, title);
    } else {
        console.log(`${title}:`, message);
        alert(`${title}: ${message}`);
    }
}

// ========================================
// EXPORTACIÓN DE FUNCIONES GLOBALES
// ========================================

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