// ========================================
// EJEMPLOS DE USO DE GUARDIAS POR PÁGINA
// ========================================

// Este archivo muestra ejemplos de cómo usar las guardias
// para evitar errores de elementos no encontrados

// Ejemplo 1: Inicialización específica por página
function initializePageSpecific() {
    const guard = new DOMGuard();
    
    // Solo ejecutar en el dashboard
    guard.executeOnDashboard(() => {
        console.log('Inicializando dashboard...');
        
        // Cargar datos del dashboard
        guard.safeExecute('#totalProducts', (element) => {
            console.log('Elemento totalProducts encontrado:', element);
        });
        
        // Agregar event listeners solo si los elementos existen
        guard.safeAddEventListener('#dashboard', 'click', () => {
            console.log('Dashboard clickeado');
        });
    });
    
    // Solo ejecutar en el login
    guard.executeOnLogin(() => {
        console.log('Inicializando página de login...');
        
        // Auto-focus en el campo de usuario
        guard.safeExecute('#username', (usernameField) => {
            usernameField.focus();
        });
        
        // Agregar event listener al formulario
        guard.safeAddEventListener('#loginForm', 'submit', (e) => {
            e.preventDefault();
            console.log('Formulario de login enviado');
        });
    });
    
    // Solo ejecutar en el perfil
    guard.executeOnProfile(() => {
        console.log('Inicializando página de perfil...');
        
        // Cargar datos del usuario
        guard.safeExecute('#profileForm', (form) => {
            console.log('Formulario de perfil encontrado:', form);
        });
    });
    
    // Solo ejecutar en cambio de contraseña
    guard.executeOnChangePassword(() => {
        console.log('Inicializando página de cambio de contraseña...');
        
        // Validar formulario de cambio de contraseña
        guard.safeExecute('#changePasswordForm', (form) => {
            console.log('Formulario de cambio de contraseña encontrado:', form);
        });
    });
}

// Ejemplo 2: Event listeners seguros
function setupSafeEventListeners() {
    const guard = new DOMGuard();
    
    // Agregar event listeners solo si los elementos existen
    guard.safeAddEventListener('#submitBtn', 'click', () => {
        console.log('Botón de envío clickeado');
    });
    
    // Agregar múltiples event listeners de forma segura
    const selectors = ['#btn1', '#btn2', '#btn3'];
    guard.safeAddEventListeners(selectors, 'click', (e) => {
        console.log('Botón clickeado:', e.target.id);
    });
    
    // Ejecutar función solo si el elemento existe
    guard.safeExecute('#importantElement', (element) => {
        console.log('Elemento importante encontrado:', element);
        element.classList.add('highlighted');
    }, () => {
        console.log('Elemento importante no encontrado, usando fallback');
    });
}

// Ejemplo 3: Código que se ejecuta en múltiples páginas
function setupCommonFunctionality() {
    const guard = new DOMGuard();
    
    // Ejecutar en dashboard y perfil
    guard.executeOnPages(['dashboard', 'profile'], () => {
        console.log('Configurando funcionalidad común para dashboard y perfil');
        
        // Agregar event listener para logout
        guard.safeAddEventListener('.logout-btn', 'click', () => {
            console.log('Logout solicitado');
            authManager.logout();
        });
    });
    
    // Ejecutar en todas las páginas excepto login
    guard.executeOnPagesExcept(['login'], () => {
        console.log('Configurando funcionalidad para páginas autenticadas');
        
        // Verificar autenticación
        if (!authManager.isAuthenticated()) {
            window.location.href = '/login';
        }
    });
}

// Ejemplo 4: Inicialización condicional
function conditionalInitialization() {
    const guard = new DOMGuard();
    
    // Inicializar según la página actual
    switch (guard.pageDetector.getCurrentPage()) {
        case 'dashboard':
            initializeDashboard();
            break;
        case 'login':
            initializeLogin();
            break;
        case 'profile':
            initializeProfile();
            break;
        default:
            console.log('Página no reconocida, inicialización básica');
            break;
    }
}

// Funciones de inicialización específicas
function initializeDashboard() {
    const guard = new DOMGuard();
    console.log('Inicializando dashboard...');
    
    // Solo ejecutar si estamos en el dashboard
    guard.executeOnDashboard(() => {
        // Cargar datos del dashboard
        updateDashboard();
        
        // Configurar navegación
        setupNavigation();
        
        // Configurar búsquedas
        setupSearch();
    });
}

function initializeLogin() {
    const guard = new DOMGuard();
    console.log('Inicializando página de login...');
    
    // Solo ejecutar si estamos en el login
    guard.executeOnLogin(() => {
        // Auto-focus en el primer campo
        guard.safeExecute('#username', (field) => field.focus());
        
        // Configurar formulario
        setupLoginForm();
    });
}

function initializeProfile() {
    const guard = new DOMGuard();
    console.log('Inicializando página de perfil...');
    
    // Solo ejecutar si estamos en el perfil
    guard.executeOnProfile(() => {
        // Cargar datos del usuario
        loadUserProfile();
        
        // Configurar formulario de edición
        setupProfileForm();
    });
}

// Funciones auxiliares
function setupNavigation() {
    const guard = new DOMGuard();
    
    guard.safeAddEventListener('.nav-toggle', 'click', () => {
        guard.safeExecute('.nav-menu', (menu) => {
            menu.classList.toggle('active');
        });
    });
}

function setupSearch() {
    const guard = new DOMGuard();
    
    guard.safeAddEventListener('#productSearch', 'input', filterProducts);
    guard.safeAddEventListener('#categoryFilter', 'change', filterProducts);
}

function setupLoginForm() {
    const guard = new DOMGuard();
    
    guard.safeAddEventListener('#loginForm', 'submit', async (e) => {
        e.preventDefault();
        // Lógica de login
    });
}

function loadUserProfile() {
    const guard = new DOMGuard();
    
    guard.safeExecute('#userInfo', (element) => {
        // Cargar información del usuario
        console.log('Cargando perfil del usuario');
    });
}

function setupProfileForm() {
    const guard = new DOMGuard();
    
    guard.safeAddEventListener('#profileForm', 'submit', (e) => {
        e.preventDefault();
        // Lógica de actualización de perfil
    });
}

// Exportar funciones para uso global
window.initializePageSpecific = initializePageSpecific;
window.setupSafeEventListeners = setupSafeEventListeners;
window.setupCommonFunctionality = setupCommonFunctionality;
window.conditionalInitialization = conditionalInitialization;
