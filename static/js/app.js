// Configuración de la API
const API_BASE_URL = 'http://127.0.0.1:8080/api';

// Clase principal de la aplicación
class StockManagementApp {
    constructor() {
        this.currentTab = 'dashboard';
        this.categories = [];
        this.products = [];
        this.stock = [];
        this.orders = [];
        this.purchases = [];
        
        this.init();
    }

    async init() {
        this.setupTheme();
        this.setupEventListeners();
        await this.loadDashboardData();
        this.showTab('dashboard');
    }

    setupTheme() {
        // Verificar si hay un tema guardado en localStorage
        const savedTheme = localStorage.getItem('theme') || 'light';
        this.setTheme(savedTheme);
        
        // Configurar el botón de cambio de tema
        const themeToggle = document.getElementById('themeToggle');
        const themeIcon = document.getElementById('themeIcon');
        
        if (themeToggle && themeIcon) {
            themeToggle.addEventListener('click', () => {
                const currentTheme = document.documentElement.getAttribute('data-theme');
                const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
                this.setTheme(newTheme);
            });
        }
    }

    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        
        // Actualizar el icono del botón
        const themeIcon = document.getElementById('themeIcon');
        if (themeIcon) {
            if (theme === 'dark') {
                themeIcon.className = 'fas fa-sun';
                themeIcon.parentElement.title = 'Cambiar a modo claro';
            } else {
                themeIcon.className = 'fas fa-moon';
                themeIcon.parentElement.title = 'Cambiar a modo oscuro';
            }
        }
    }

    setupEventListeners() {
        // Navegación por pestañas
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                const tabName = e.target.dataset.tab;
                this.showTab(tabName);
            });
        });

        // Formularios
        this.setupFormListeners();
        
        // Modales
        this.setupModalListeners();
    }

    setupModalListeners() {
        // Cerrar modales
        document.querySelectorAll('.close').forEach(closeBtn => {
            closeBtn.addEventListener('click', () => {
                this.closeAllModals();
            });
        });

        // Cerrar modales al hacer clic fuera
        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.closeAllModals();
            }
        });

        // Formularios de edición
        const editCategoryForm = document.getElementById('editCategoryForm');
        if (editCategoryForm) {
            editCategoryForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.updateCategory();
            });
        }

        const editProductForm = document.getElementById('editProductForm');
        if (editProductForm) {
            editProductForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.updateProduct();
            });
        }

        const editStockForm = document.getElementById('editStockForm');
        if (editStockForm) {
            editStockForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.updateStockFromModal();
            });
        }
    }

    setupFormListeners() {
        // Formulario de categorías
        const categoryForm = document.getElementById('categoryForm');
        if (categoryForm) {
            categoryForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.createCategory();
            });
        }

        // Formulario de productos
        const productForm = document.getElementById('productForm');
        if (productForm) {
            productForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.createProduct();
            });
        }

        // Formulario de órdenes de compra
        const purchaseForm = document.getElementById('purchaseForm');
        if (purchaseForm) {
            purchaseForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.createPurchaseOrder();
            });
        }

        // Formulario de órdenes de venta
        const orderForm = document.getElementById('orderForm');
        if (orderForm) {
            orderForm.addEventListener('submit', (e) => {
                e.preventDefault();
                
                // Verificar si hay productos agregados
                const itemsInput = document.getElementById('orderItemsInput');
                const items = JSON.parse(itemsInput.value || '[]');
                
                if (items.length === 0) {
                    this.showAlert('Debe agregar al menos un producto antes de crear la orden', 'error');
                    return;
                }
                
                // Si hay productos, permitir la creación de la orden
                this.createOrder();
            });
        }
    }

    closeAllModals() {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.style.display = 'none';
        });
    }

    async loadDashboardData() {
        try {
            await Promise.all([
                this.loadCategories(),
                this.loadProducts(),
                this.loadStock(),
                this.loadPurchases()
            ]);
            this.updateDashboard();
        } catch (error) {
            console.error('Error cargando datos del dashboard:', error);
            this.showAlert('Error cargando datos del dashboard', 'error');
        }
    }

    async loadCategories() {
        try {
            const response = await fetch(`${API_BASE_URL}/categories/`);
            if (response.ok) {
                this.categories = await response.json();
            }
        } catch (error) {
            console.error('Error cargando categorías:', error);
        }
    }

    async loadProducts() {
        try {
            const response = await fetch(`${API_BASE_URL}/products/`);
            if (response.ok) {
                this.products = await response.json();
            }
        } catch (error) {
            console.error('Error cargando productos:', error);
        }
    }

    async loadStock() {
        try {
            const response = await fetch(`${API_BASE_URL}/stock/`);
            if (response.ok) {
                this.stock = await response.json();
            }
        } catch (error) {
            console.error('Error cargando stock:', error);
        }
    }

    async loadOrders() {
        try {
            const response = await fetch(`${API_BASE_URL}/orders/`);
            if (response.ok) {
                this.orders = await response.json();
            }
        } catch (error) {
            console.error('Error cargando órdenes:', error);
        }
    }

    async loadPurchases() {
        try {
            const response = await fetch(`${API_BASE_URL}/purchases/`);
            if (response.ok) {
                this.purchases = await response.json();
            }
        } catch (error) {
            console.error('Error cargando órdenes de compra:', error);
        }
    }

    showTab(tabName) {
        // Ocultar todas las pestañas
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.classList.remove('active');
        });

        // Mostrar la pestaña seleccionada
        const selectedTab = document.querySelector(`[data-tab="${tabName}"]`);
        const selectedContent = document.getElementById(`${tabName}Content`);
        
        if (selectedTab && selectedContent) {
            selectedTab.classList.add('active');
            selectedContent.classList.add('active');
            this.currentTab = tabName;
            
            // Cargar datos específicos de la pestaña
            this.loadTabData(tabName);
        }
    }

    async loadTabData(tabName) {
        switch (tabName) {
            case 'categories':
                await this.loadCategories();
                this.renderCategories();
                break;
            case 'products':
                await this.loadCategories();
                await this.loadProducts();
                this.renderProducts();
                this.fillProductCategorySelect(); // Llenar el select de categorías
                break;
            case 'stock':
                await this.loadStock();
                this.renderStock();
                break;
            case 'orders':
                await this.loadProducts(); // Cargar productos para el select
                await this.loadPurchases();
                this.renderOrders();
                this.fillOrderProductSelect(); // Llenar el select de productos
                this.updateCreateOrderButton(); // Actualizar estado del botón
                break;
            case 'purchases':
                await this.loadProducts(); // Cargar productos para el select
                await this.loadPurchases();
                this.renderPurchases();
                this.fillPurchaseProductSelect(); // Llenar el select de productos
                break;
        }
    }

    async createCategory() {
        const form = document.getElementById('categoryForm');
        const formData = new FormData(form);
        const categoryData = {
            name: formData.get('name')
        };

        try {
            const response = await fetch(`${API_BASE_URL}/categories/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(categoryData)
            });

            if (response.ok) {
                this.showAlert('Categoría creada exitosamente', 'success');
                form.reset();
                await this.loadCategories();
                this.renderCategories();
                this.updateDashboard();
                
                // Si estamos en la pestaña de productos, actualizar el select de categorías
                if (this.currentTab === 'products') {
                    this.fillProductCategorySelect();
                }
            } else {
                const error = await response.json();
                this.showAlert(`Error: ${error.message || 'Error desconocido'}`, 'error');
            }
        } catch (error) {
            console.error('Error creando categoría:', error);
            this.showAlert('Error de conexión', 'error');
        }
    }

    async updateCategory() {
        const form = document.getElementById('editCategoryForm');
        const categoryId = document.getElementById('editCategoryId').value;
        const categoryName = document.getElementById('editCategoryName').value;

        try {
            const response = await fetch(`${API_BASE_URL}/categories/${categoryId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name: categoryName })
            });

            if (response.ok) {
                this.showAlert('Categoría actualizada exitosamente', 'success');
                this.closeAllModals();
                await this.loadCategories();
                this.renderCategories();
                this.updateDashboard();
                
                // Si estamos en la pestaña de productos, actualizar el select de categorías
                if (this.currentTab === 'products') {
                    this.fillProductCategorySelect();
                }
            } else {
                const error = await response.json();
                this.showAlert(`Error: ${error.message || 'Error desconocido'}`, 'error');
            }
        } catch (error) {
            console.error('Error actualizando categoría:', error);
            this.showAlert('Error de conexión', 'error');
        }
    }

    async deleteCategory(id) {
        if (!confirm('¿Está seguro de que desea eliminar esta categoría?')) {
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/categories/${id}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                this.showAlert('Categoría eliminada exitosamente', 'success');
                await this.loadCategories();
                this.renderCategories();
                this.updateDashboard();
                
                // Si estamos en la pestaña de productos, actualizar el select de categorías
                if (this.currentTab === 'products') {
                    this.fillProductCategorySelect();
                }
            } else {
                const error = await response.json();
                this.showAlert(`Error: ${error.message || 'Error desconocido'}`, 'error');
            }
        } catch (error) {
            console.error('Error eliminando categoría:', error);
            this.showAlert('Error de conexión', 'error');
        }
    }

    editCategory(id) {
        const category = this.categories.find(c => c.id === id);
        if (!category) return;

        document.getElementById('editCategoryId').value = category.id;
        document.getElementById('editCategoryName').value = category.name;
        document.getElementById('editCategoryModal').style.display = 'block';
    }

    async createProduct() {
        const form = document.getElementById('productForm');
        const formData = new FormData(form);
        const productData = {
            name: formData.get('name'),
            description: formData.get('description'),
            price: parseFloat(formData.get('price')),
            category_id: parseInt(formData.get('category_id')),
            min_stock: parseInt(formData.get('min_stock') || 0)
        };

        try {
            const response = await fetch(`${API_BASE_URL}/products/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(productData)
            });

            if (response.ok) {
                this.showAlert('Producto creado exitosamente', 'success');
                form.reset();
                await this.loadProducts();
                this.renderProducts();
                this.updateDashboard();
                
                // Si estamos en las pestañas de órdenes o compras, actualizar los selects de productos
                if (this.currentTab === 'orders') {
                    this.fillOrderProductSelect();
                } else if (this.currentTab === 'purchases') {
                    this.fillPurchaseProductSelect();
                }
            } else {
                const error = await response.json();
                this.showAlert(`Error: ${error.message || 'Error desconocido'}`, 'error');
            }
        } catch (error) {
            console.error('Error creando producto:', error);
            this.showAlert('Error de conexión', 'error');
        }
    }

    async updateProduct() {
        const form = document.getElementById('editProductForm');
        const productId = document.getElementById('editProductId').value;
        const productData = {
            name: document.getElementById('editProductName').value,
            description: document.getElementById('editProductDescription').value,
            price: parseFloat(document.getElementById('editProductPrice').value),
            category_id: parseInt(document.getElementById('editProductCategory').value),
            min_stock: parseInt(document.getElementById('editProductMinStock').value || 0)
        };

        try {
            const response = await fetch(`${API_BASE_URL}/products/${productId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(productData)
            });

            if (response.ok) {
                this.showAlert('Producto actualizado exitosamente', 'success');
                this.closeAllModals();
                await this.loadProducts();
                await this.loadStock();
                this.renderProducts();
                this.renderStock();
                this.updateDashboard();
                
                // Si estamos en las pestañas de órdenes o compras, actualizar los selects de productos
                if (this.currentTab === 'orders') {
                    this.fillOrderProductSelect();
                } else if (this.currentTab === 'purchases') {
                    this.fillPurchaseProductSelect();
                }
            } else {
                const error = await response.json();
                this.showAlert(`Error: ${error.message || 'Error desconocido'}`, 'error');
            }
        } catch (error) {
            console.error('Error actualizando producto:', error);
            this.showAlert('Error de conexión', 'error');
        }
    }

    async deleteProduct(id) {
        if (!confirm('¿Está seguro de que desea eliminar este producto?')) {
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/products/${id}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                this.showAlert('Producto eliminado exitosamente', 'success');
                await this.loadProducts();
                await this.loadStock();
                this.renderProducts();
                this.renderStock();
                this.updateDashboard();
                
                // Si estamos en las pestañas de órdenes o compras, actualizar los selects de productos
                if (this.currentTab === 'orders') {
                    this.fillOrderProductSelect();
                } else if (this.currentTab === 'purchases') {
                    this.fillPurchaseProductSelect();
                }
            } else {
                const error = await response.json();
                this.showAlert(`Error: ${error.message || 'Error desconocido'}`, 'error');
            }
        } catch (error) {
            console.error('Error eliminando producto:', error);
            this.showAlert('Error de conexión', 'error');
        }
    }

    editProduct(id) {
        const product = this.products.find(p => p.id === id);
        if (!product) return;

        document.getElementById('editProductId').value = product.id;
        document.getElementById('editProductName').value = product.name;
        document.getElementById('editProductDescription').value = product.description;
        document.getElementById('editProductPrice').value = product.price;
        document.getElementById('editProductCategory').value = product.category_id;
        
        // Cargar categorías en el select
        const categorySelect = document.getElementById('editProductCategory');
        categorySelect.innerHTML = '<option value="">Seleccionar categoría</option>';
        this.categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category.id;
            option.textContent = category.name;
            if (category.id === product.category_id) {
                option.selected = true;
            }
            categorySelect.appendChild(option);
        });

        // Cargar stock mínimo
        const stock = this.stock.find(s => s.product_id === product.id);
        if (stock) {
            document.getElementById('editProductMinStock').value = stock.min_stock;
        }

        document.getElementById('editProductModal').style.display = 'block';
    }

    async createPurchaseOrder() {
        const form = document.getElementById('purchaseForm');
        const formData = new FormData(form);
        const items = JSON.parse(formData.get('items') || '[]');

        if (items.length === 0) {
            this.showAlert('Debe agregar al menos un producto', 'error');
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/purchases/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ items })
            });

            if (response.ok) {
                this.showAlert('Orden de compra creada exitosamente', 'success');
                form.reset();
                document.getElementById('purchaseItems').innerHTML = '';
                document.getElementById('purchaseItemsInput').value = '[]';
                await this.loadPurchases();
                this.renderPurchases();
                this.updateDashboard();
            } else {
                const error = await response.json();
                this.showAlert(`Error: ${error.message || 'Error desconocido'}`, 'error');
            }
        } catch (error) {
            console.error('Error creando orden de compra:', error);
            this.showAlert('Error de conexión', 'error');
        }
    }

    async createOrder() {
        const form = document.getElementById('orderForm');
        const itemsInput = document.getElementById('orderItemsInput');
        const items = JSON.parse(itemsInput.value || '[]');

        if (items.length === 0) {
            this.showAlert('Debe agregar al menos un producto', 'error');
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/purchases/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ items })
            });

            if (response.ok) {
                this.showAlert('Orden de compra creada exitosamente', 'success');
                form.reset();
                document.getElementById('orderItems').innerHTML = '';
                document.getElementById('orderItemsInput').value = '[]';
                
                // Deshabilitar el botón de crear orden
                this.updateCreateOrderButton();
                
                await this.loadPurchases();
                this.renderOrders();
                this.updateDashboard();
            } else {
                const error = await response.json();
                this.showAlert(`Error: ${error.message || 'Error desconocido'}`, 'error');
            }
        } catch (error) {
            console.error('Error creando orden de compra:', error);
            this.showAlert('Error de conexión', 'error');
        }
    }

    async completePurchaseOrder(id) {
        try {
            const response = await fetch(`${API_BASE_URL}/purchases/${id}/complete`, {
                method: 'PUT'
            });

            if (response.ok) {
                this.showAlert('Orden de compra completada exitosamente', 'success');
                await this.loadPurchases();
                await this.loadStock();
                
                // Actualizar ambas vistas
                this.renderOrders(); // Solo mostrará órdenes pendientes
                this.renderPurchases(); // Mostrará todas las órdenes
                this.updateDashboard();
            } else {
                const error = await response.json();
                this.showAlert(`Error: ${error.message || 'Error desconocido'}`, 'error');
            }
        } catch (error) {
            console.error('Error completando orden de compra:', error);
            this.showAlert('Error de conexión', 'error');
        }
    }

    async completeOrder(id) {
        try {
            const response = await fetch(`${API_BASE_URL}/orders/${id}/complete`, {
                method: 'PUT'
            });

            if (response.ok) {
                this.showAlert('Orden completada exitosamente', 'success');
                await this.loadOrders();
                await this.loadStock();
                this.renderOrders();
                this.renderStock();
                this.updateDashboard();
            } else {
                const error = await response.json();
                this.showAlert(`Error: ${error.message || 'Error desconocido'}`, 'error');
            }
        } catch (error) {
            console.error('Error completando orden:', error);
            this.showAlert('Error de conexión', 'error');
        }
    }

    async deleteOrder(id) {
        if (!confirm('¿Está seguro de que desea eliminar esta orden?')) {
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/orders/${id}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                this.showAlert('Orden eliminada exitosamente', 'success');
                await this.loadOrders();
                this.renderOrders();
                this.updateDashboard();
            } else {
                const error = await response.json();
                this.showAlert(`Error: ${error.message || 'Error desconocido'}`, 'error');
            }
        } catch (error) {
            console.error('Error eliminando orden:', error);
            this.showAlert('Error de conexión', 'error');
        }
    }

    async deletePurchaseOrder(id) {
        if (!confirm('¿Está seguro de que desea eliminar esta orden de compra?')) {
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/purchases/${id}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                this.showAlert('Orden de compra eliminada exitosamente', 'success');
                await this.loadPurchases();
                
                // Actualizar ambas vistas
                this.renderOrders(); // Solo mostrará órdenes pendientes
                this.renderPurchases(); // Mostrará todas las órdenes
                this.updateDashboard();
            } else {
                const error = await response.json();
                this.showAlert(`Error: ${error.message || 'Error desconocido'}`, 'error');
            }
        } catch (error) {
            console.error('Error eliminando orden de compra:', error);
            this.showAlert('Error de conexión', 'error');
        }
    }

    async updateStock(productId, quantity, minStock) {
        try {
            const response = await fetch(`${API_BASE_URL}/stock/${productId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ quantity, min_stock: minStock })
            });

            if (response.ok) {
                this.showAlert('Stock actualizado exitosamente', 'success');
                await this.loadStock();
                this.renderStock();
                this.updateDashboard();
            } else {
                const error = await response.json();
                this.showAlert(`Error: ${error.message || 'Error desconocido'}`, 'error');
            }
        } catch (error) {
            console.error('Error actualizando stock:', error);
            this.showAlert('Error de conexión', 'error');
        }
    }

    async updateStockFromModal() {
        const productId = document.getElementById('editStockProductId').value;
        const quantity = parseInt(document.getElementById('editStockQuantity').value);
        const minStock = parseInt(document.getElementById('editStockMinStock').value);

        await this.updateStock(productId, quantity, minStock);
        this.closeAllModals();
    }

    editStock(productId) {
        const stock = this.stock.find(s => s.product_id === productId);
        const product = this.products.find(p => p.id === productId);
        
        if (!stock || !product) return;

        document.getElementById('editStockProductId').value = productId;
        document.getElementById('editStockQuantity').value = stock.quantity;
        document.getElementById('editStockMinStock').value = stock.min_stock;
        
        document.getElementById('editStockModal').style.display = 'block';
    }

    renderCategories() {
        const container = document.getElementById('categoriesTable');
        if (!container) return;

        const html = `
            <div class="table-container">
                <table class="table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Productos</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${this.categories.map(category => `
                            <tr>
                                <td>${category.id}</td>
                                <td>${category.name}</td>
                                <td>${this.products.filter(p => p.category_id === category.id).length}</td>
                                <td>
                                    <button class="btn btn-edit btn-sm" onclick="app.editCategory(${category.id})">
                                        <i class="fas fa-edit"></i> Editar
                                    </button>
                                    <button class="btn btn-delete btn-sm" onclick="app.deleteCategory(${category.id})">
                                        <i class="fas fa-trash"></i> Eliminar
                                    </button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
        container.innerHTML = html;
    }

    renderProducts() {
        const container = document.getElementById('productsTable');
        if (!container) return;

        const html = `
            <div class="table-container">
                <table class="table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Descripción</th>
                            <th>Precio</th>
                            <th>Categoría</th>
                            <th>Stock</th>
                            <th>Stock Mínimo</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${this.products.map(product => {
                            const stock = this.stock.find(s => s.product_id === product.id);
                            const category = this.categories.find(c => c.id === product.category_id);
                            return `
                                <tr>
                                    <td>${product.id}</td>
                                    <td>${product.name}</td>
                                    <td>${product.description}</td>
                                    <td>$${product.price.toFixed(2)}</td>
                                    <td>${category ? category.name : 'N/A'}</td>
                                    <td>${stock ? stock.quantity : 0}</td>
                                    <td>${stock ? stock.min_stock : 0}</td>
                                    <td>
                                        <button class="btn btn-edit btn-sm" onclick="app.editProduct(${product.id})">
                                            <i class="fas fa-edit"></i> Editar
                                        </button>
                                        <button class="btn btn-delete btn-sm" onclick="app.deleteProduct(${product.id})">
                                            <i class="fas fa-trash"></i> Eliminar
                                        </button>
                                    </td>
                                </tr>
                            `;
                        }).join('')}
                    </tbody>
                </table>
            </div>
        `;
        container.innerHTML = html;
    }

    renderStock() {
        const container = document.getElementById('stockTable');
        if (!container) return;

        const html = `
            <div class="table-container">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Producto</th>
                            <th>Stock Actual</th>
                            <th>Stock Mínimo</th>
                            <th>Estado</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${this.stock.map(stock => {
                            const product = this.products.find(p => p.id === stock.product_id);
                            const status = stock.quantity <= stock.min_stock ? 'danger' : 'success';
                            const statusText = stock.quantity <= stock.min_stock ? 'Bajo Stock' : 'OK';
                            
                            return `
                                <tr>
                                    <td>${product ? product.name : 'N/A'}</td>
                                    <td>${stock.quantity}</td>
                                    <td>${stock.min_stock}</td>
                                    <td><span class="status ${status}">${statusText}</span></td>
                                    <td>
                                        <button class="btn btn-primary btn-sm" onclick="app.editStock(${stock.product_id})">
                                            <i class="fas fa-edit"></i> Editar
                                        </button>
                                    </td>
                                </tr>
                            `;
                        }).join('')}
                    </tbody>
                </table>
            </div>
        `;
        container.innerHTML = html;
    }

    renderOrders() {
        const container = document.getElementById('ordersTable');
        if (!container) return;

        // Filtrar solo órdenes pendientes
        const pendingOrders = this.purchases.filter(purchase => purchase.status === 'pending');

        if (pendingOrders.length === 0) {
            container.innerHTML = `
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i>
                    No hay órdenes de compra pendientes. Todas las órdenes han sido completadas o eliminadas.
                </div>
            `;
            return;
        }

        const html = `
            <div class="table-container">
                <table class="table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Productos</th>
                            <th>Estado</th>
                            <th>Fecha</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${pendingOrders.map(purchase => {
                            const itemsText = purchase.items ? purchase.items.map(item => 
                                `${item.product_name} (${item.quantity})`
                            ).join(', ') : 'N/A';
                            
                            return `
                                <tr>
                                    <td>${purchase.id}</td>
                                    <td>${itemsText}</td>
                                    <td><span class="status ${purchase.status}">${purchase.status}</span></td>
                                    <td>${new Date(purchase.created_at).toLocaleDateString()}</td>
                                    <td>
                                        <button class="btn btn-success btn-sm" onclick="app.completePurchaseOrder(${purchase.id})">
                                            <i class="fas fa-check"></i> Completar
                                        </button>
                                        <button class="btn btn-delete btn-sm" onclick="app.deletePurchaseOrder(${purchase.id})">
                                            <i class="fas fa-trash"></i> Eliminar
                                        </button>
                                    </td>
                                </tr>
                            `;
                        }).join('')}
                    </tbody>
                </table>
            </div>
        `;
        container.innerHTML = html;
    }

    renderPurchases() {
        const container = document.getElementById('purchasesTable');
        if (!container) return;

        // Filtrar solo órdenes completadas
        const completedOrders = this.purchases.filter(purchase => purchase.status === 'completed');

        if (completedOrders.length === 0) {
            container.innerHTML = `
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i>
                    No hay órdenes de compra completadas. Las órdenes aparecerán aquí una vez que sean completadas desde la sección de Órdenes.
                </div>
            `;
            return;
        }

        const html = `
            <div class="table-container">
                <table class="table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Productos</th>
                            <th>Estado</th>
                            <th>Fecha de Completado</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${completedOrders.map(purchase => {
                            const itemsText = purchase.items ? purchase.items.map(item => 
                                `${item.product_name} (${item.quantity})`
                            ).join(', ') : 'N/A';
                            
                            return `
                                <tr>
                                    <td>${purchase.id}</td>
                                    <td>${itemsText}</td>
                                    <td><span class="status completed">Completada</span></td>
                                    <td>${new Date(purchase.created_at).toLocaleDateString()}</td>
                                </tr>
                            `;
                        }).join('')}
                    </tbody>
                </table>
            </div>
        `;
        container.innerHTML = html;
    }

    updateDashboard() {
        const totalProducts = this.products.length;
        const totalCategories = this.categories.length;
        const lowStockProducts = this.stock.filter(s => s.quantity <= s.min_stock).length;
        const pendingPurchases = this.purchases.filter(p => p.status === 'pending').length;

        // Actualizar estadísticas del dashboard
        const statsContainer = document.getElementById('dashboardStats');
        if (statsContainer) {
            statsContainer.innerHTML = `
                <div class="row">
                    <div class="col">
                        <h3>${totalProducts}</h3>
                        <p>Total Productos</p>
                    </div>
                    <div class="col">
                        <h3>${totalCategories}</h3>
                        <p>Total Categorías</p>
                    </div>
                    <div class="col">
                        <h3>${lowStockProducts}</h3>
                        <p>Productos con Bajo Stock</p>
                    </div>
                    <div class="col">
                        <h3>${pendingPurchases}</h3>
                        <p>Órdenes de Compra Pendientes</p>
                    </div>
                </div>
            `;
        }

        // Actualizar gráfico de stock
        this.updateStockChart();
    }

    updateStockChart() {
        const chartContainer = document.getElementById('stockChart');
        if (!chartContainer) return;

        const lowStockProducts = this.products.filter(product => {
            const stock = this.stock.find(s => s.product_id === product.id);
            return stock && stock.quantity <= stock.min_stock;
        });

        if (lowStockProducts.length > 0) {
            chartContainer.innerHTML = `
                <h3>Productos con Bajo Stock</h3>
                <div class="table-container">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Producto</th>
                                <th>Stock Actual</th>
                                <th>Stock Mínimo</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${lowStockProducts.map(product => {
                                const stock = this.stock.find(s => s.product_id === product.id);
                                return `
                                    <tr>
                                        <td>${product.name}</td>
                                        <td>${stock.quantity}</td>
                                        <td>${stock.min_stock}</td>
                                    </tr>
                                `;
                            }).join('')}
                        </tbody>
                    </table>
                </div>
            `;
        } else {
            chartContainer.innerHTML = `
                <div class="alert alert-success">
                    ¡Excelente! Todos los productos tienen stock suficiente.
                </div>
            `;
        }
    }

    showAlert(message, type = 'info') {
        const alertContainer = document.getElementById('alertContainer');
        if (!alertContainer) return;

        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.textContent = message;

        alertContainer.appendChild(alert);

        // Auto-remover después de 5 segundos
        setTimeout(() => {
            if (alert.parentNode) {
                alert.parentNode.removeChild(alert);
            }
        }, 5000);
    }

    addOrderItem() {
        const productSelect = document.getElementById('orderProduct');
        const quantityInput = document.getElementById('orderQuantity');
        const itemsContainer = document.getElementById('orderItems');
        const itemsInput = document.getElementById('orderItemsInput');

        const productId = productSelect.value;
        const quantity = parseInt(quantityInput.value);

        if (!productId || !quantity || quantity <= 0) {
            this.showAlert('Por favor complete todos los campos correctamente', 'error');
            return;
        }

        const product = this.products.find(p => p.id === parseInt(productId));
        if (!product) return;

        const item = { product_id: parseInt(productId), quantity };
        const currentItems = JSON.parse(itemsInput.value || '[]');
        currentItems.push(item);
        itemsInput.value = JSON.stringify(currentItems);

        const itemElement = document.createElement('div');
        itemElement.className = 'order-item';
        itemElement.innerHTML = `
            <span>${product.name} - Cantidad: ${quantity}</span>
            <button type="button" class="btn btn-danger btn-sm" onclick="this.parentElement.remove(); app.updateOrderItems();">
                Eliminar
            </button>
        `;

        itemsContainer.appendChild(itemElement);
        productSelect.value = '';
        quantityInput.value = '';
        
        // Remover la validación required de los campos
        productSelect.removeAttribute('required');
        quantityInput.removeAttribute('required');
        
        // Habilitar el botón de crear orden
        this.updateCreateOrderButton();
    }

    updateOrderItems() {
        const itemsContainer = document.getElementById('orderItems');
        const itemsInput = document.getElementById('orderItemsInput');
        const productSelect = document.getElementById('orderProduct');
        const quantityInput = document.getElementById('orderQuantity');
        const items = [];

        itemsContainer.querySelectorAll('.order-item').forEach(item => {
            const text = item.querySelector('span').textContent;
            const match = text.match(/(.+) - Cantidad: (\d+)/);
            if (match) {
                const productName = match[1];
                const quantity = parseInt(match[2]);
                const product = this.products.find(p => p.name === productName);
                if (product) {
                    items.push({ product_id: product.id, quantity });
                }
            }
        });

        itemsInput.value = JSON.stringify(items);
        
        // Actualizar el estado del botón de crear orden
        this.updateCreateOrderButton();
        
        // Si no hay items, restaurar la validación required
        if (items.length === 0) {
            productSelect.setAttribute('required', '');
            quantityInput.setAttribute('required', '');
        }
    }

    fillProductCategorySelect() {
        const categorySelect = document.getElementById('productCategory');
        if (!categorySelect) return;

        categorySelect.innerHTML = '<option value="">Seleccionar categoría</option>';
        this.categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category.id;
            option.textContent = category.name;
            categorySelect.appendChild(option);
        });
    }

    fillOrderProductSelect() {
        const productSelect = document.getElementById('orderProduct');
        if (!productSelect) return;

        productSelect.innerHTML = '<option value="">Seleccionar producto</option>';
        this.products.forEach(product => {
            const option = document.createElement('option');
            option.value = product.id;
            option.textContent = `${product.name} - $${product.price.toFixed(2)}`;
            productSelect.appendChild(option);
        });
    }

    updateCreateOrderButton() {
        const createOrderBtn = document.getElementById('createOrderBtn');
        const itemsContainer = document.getElementById('orderItems');
        
        if (!createOrderBtn || !itemsContainer) return;
        
        // Contar cuántos items hay en la orden
        const itemCount = itemsContainer.querySelectorAll('.order-item').length;
        
        if (itemCount > 0) {
            createOrderBtn.disabled = false;
            createOrderBtn.title = `Crear orden con ${itemCount} producto${itemCount > 1 ? 's' : ''}`;
        } else {
            createOrderBtn.disabled = true;
            createOrderBtn.title = 'Agrega al menos un producto para crear la orden';
        }
    }

    addPurchaseItem() {
        const productSelect = document.getElementById('purchaseProduct');
        const quantityInput = document.getElementById('purchaseQuantity');
        const itemsContainer = document.getElementById('purchaseItems');
        const itemsInput = document.getElementById('purchaseItemsInput');

        const productId = productSelect.value;
        const quantity = parseInt(quantityInput.value);

        if (!productId || !quantity || quantity <= 0) {
            this.showAlert('Por favor complete todos los campos correctamente', 'error');
            return;
        }

        const product = this.products.find(p => p.id === parseInt(productId));
        if (!product) return;

        const item = { product_id: parseInt(productId), quantity };
        const currentItems = JSON.parse(itemsInput.value || '[]');
        currentItems.push(item);
        itemsInput.value = JSON.stringify(currentItems);

        const itemElement = document.createElement('div');
        itemElement.className = 'order-item';
        itemElement.innerHTML = `
            <span>${product.name} - Cantidad: ${quantity}</span>
            <button type="button" class="btn btn-danger btn-sm" onclick="this.parentElement.remove(); app.updatePurchaseItems();">
                Eliminar
            </button>
        `;

        itemsContainer.appendChild(itemElement);
        productSelect.value = '';
        quantityInput.value = '';
    }

    updatePurchaseItems() {
        const itemsContainer = document.getElementById('purchaseItems');
        const itemsInput = document.getElementById('purchaseItemsInput');
        const items = [];

        itemsContainer.querySelectorAll('.order-item').forEach(item => {
            const text = item.querySelector('span').textContent;
            const match = text.match(/(.+) - Cantidad: (\d+)/);
            if (match) {
                const productName = match[1];
                const quantity = parseInt(match[2]);
                const product = this.products.find(p => p.name === productName);
                if (product) {
                    items.push({ product_id: product.id, quantity });
                }
            }
        });

        itemsInput.value = JSON.stringify(items);
    }

    fillPurchaseProductSelect() {
        const productSelect = document.getElementById('purchaseProduct');
        if (!productSelect) return;

        productSelect.innerHTML = '<option value="">Seleccionar producto</option>';
        this.products.forEach(product => {
            const option = document.createElement('option');
            option.value = product.id;
            option.textContent = `${product.name} - $${product.price.toFixed(2)}`;
            productSelect.appendChild(option);
        });
    }
}

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.app = new StockManagementApp();
}); 