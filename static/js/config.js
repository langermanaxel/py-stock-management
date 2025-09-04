// ================================
// Configuración del Frontend (fuente de la verdad)
// ================================

// Congela objetos recursivamente para evitar mutaciones accidentales
function deepFreeze(obj) {
    Object.getOwnPropertyNames(obj).forEach((name) => {
      const value = obj[name];
      if (value && typeof value === 'object') deepFreeze(value);
    });
    return Object.freeze(obj);
  }
  
  // Detectar entorno (simple)
  const IS_DEV = ['localhost', '127.0.0.1'].includes(location.hostname);
  
  // Permisos CANÓNICOS (deben coincidir con el backend)
  const PERMISSIONS = deepFreeze({
    ALL: 'all',
    MANAGE_USERS: 'manage_users',
    VIEW_REPORTS: 'view_reports',
    EDIT_PRODUCTS: 'edit_products',
    CREATE_ORDERS: 'create_orders',
    READ: 'read',
    READ_LIMITED: 'read_limited',
    READ_ONLY: 'read_only',
  });
  
  // Mapa opcional de “alias UI” -> permiso canónico (si lo necesitás)
  const PERMISSION_ALIASES = deepFreeze({
    read: PERMISSIONS.READ,
    create: PERMISSIONS.EDIT_PRODUCTS,   // ejemplo: "create" en UI = editar productos en backend
    update: PERMISSIONS.EDIT_PRODUCTS,
    create_orders: PERMISSIONS.CREATE_ORDERS,
    read_limited: PERMISSIONS.READ_LIMITED,
    read_only: PERMISSIONS.READ_ONLY,
  });
  
  // Roles y permisos alineados al backend (puede extenderse)
  const ROLES = deepFreeze({
    admin: {
      name: 'Administrador',
      level: 4,
      permissions: [PERMISSIONS.ALL],
    },
    manager: {
      name: 'Gerente',
      level: 3,
      permissions: [PERMISSIONS.VIEW_REPORTS, PERMISSIONS.EDIT_PRODUCTS],
    },
    supervisor: {
      name: 'Supervisor',
      level: 2,
      permissions: [PERMISSIONS.CREATE_ORDERS, PERMISSIONS.READ],
    },
    user: {
      name: 'Usuario',
      level: 1,
      permissions: [PERMISSIONS.READ_LIMITED],
    },
    viewer: {
      name: 'Viewer',
      level: 0,
      permissions: [PERMISSIONS.READ_ONLY],
    },
  });
  
  // Endpoints **sin** slash final (se concatenan con API_BASE_URL)
  const ENDPOINTS = deepFreeze({
    auth: {
      base: '/auth',
      login: '/auth/login',
      refresh: '/auth/refresh',
      logout: '/auth/logout',
      validate: '/auth/validate',
    },
    data: {
      categories: '/categories',
      products: '/products',
      stock: '/stock',
      orders: '/orders',
      purchases: '/purchases',
    },
  });
  
  // Config principal
  const APP_CONFIG = deepFreeze({
    API_BASE_URL: '/api', // cambia a '' si el backend expone /auth directamente
    UI: {
      TOKEN_EXPIRY_WARNING_MIN: 5,
      TOAST_DURATION_MS: 5000,
      MESSAGE_COLORS: {
        success: '#28a745',
        error: '#dc3545',
        warning: '#ffc107',
        info: '#17a2b8',
      },
    },
    CORS_DEFAULTS: {
      mode: 'cors',
      credentials: 'omit', // usamos Authorization: Bearer, no cookies
      headers: {
        Accept: 'application/json',
        // Content-Type se agrega dinámicamente si hay body JSON
        'X-Requested-With': 'XMLHttpRequest', // quítalo si no lo usás
      },
    },
    PERMISSIONS,
    PERMISSION_ALIASES,
    ROLES,
    ENDPOINTS,
    DEMO_CREDENTIALS: IS_DEV
      ? {
          admin: { username: 'admin',   password: 'Admin123!',   role: 'admin',    description: 'Acceso completo' },
          manager:{ username: 'gerente', password: 'Gerente123!', role: 'manager',  description: 'Gestión inventario' },
          user:   { username: 'usuario', password: 'Usuario123!', role: 'user',     description: 'Órdenes y lectura' },
          viewer: { username: 'viewer',  password: 'Viewer123!',  role: 'viewer',   description: 'Solo lectura' },
        }
      : null,
  });
  
  // ================================
  // Helpers de URL y fetch
  // ================================
  
  // Concatena base + path asegurando una sola barra
  function apiPath(path) {
    const base = APP_CONFIG.API_BASE_URL || '';
    if (!path) return base;
    return `${base}${path.startsWith('/') ? path : `/${path}`}`;
  }
  
  // Devuelve el endpoint absoluto de una sección/clave
  function getEndpoint(section, key) {
    const sec = APP_CONFIG.ENDPOINTS[section];
    if (!sec) throw new Error(`Sección de endpoint desconocida: ${section}`);
    const path = key ? sec[key] : sec.base || '';
    if (!path) throw new Error(`Endpoint no definido para ${section}.${key}`);
    return apiPath(path);
  }
  
  // Arma opciones de fetch según método y body (agrega Content-Type solo si hay body)
  function buildFetchInit(method = 'GET', body = undefined, extra = {}) {
    const init = {
      method,
      ...APP_CONFIG.CORS_DEFAULTS,
      ...extra,
      headers: {
        ...APP_CONFIG.CORS_DEFAULTS.headers,
        ...(extra.headers || {}),
      },
    };
    if (body !== undefined) {
      init.body = typeof body === 'string' ? body : JSON.stringify(body);
      init.headers['Content-Type'] = 'application/json';
    } else {
      // No forzar Content-Type en GET/HEAD sin body
      if (init.method === 'GET' || init.method === 'HEAD') {
        delete init.headers['Content-Type'];
      }
    }
    return init;
  }
  
  // ================================
  // Helpers de roles/permisos
  // ================================
  
  function getRoleInfo(role) {
    return APP_CONFIG.ROLES[role] || null;
  }
  
  function getRoleDisplayName(role) {
    const r = getRoleInfo(role);
    return r ? r.name : role;
  }
  
  function getRoleLevel(role) {
    const r = getRoleInfo(role);
    return r ? r.level : 0;
  }
  
  function isRoleSuperiorOrEqual(roleA, roleB) {
    return getRoleLevel(roleA) >= getRoleLevel(roleB);
  }
  
  function normalizePermission(perm) {
    // Si viene un alias tipo "read" desde la UI, lo traducimos a canónico
    return APP_CONFIG.PERMISSION_ALIASES[perm] || perm;
  }
  
  function hasRolePermission(role, permission) {
    const r = getRoleInfo(role);
    if (!r) return false;
    const canonical = normalizePermission(permission);
    if (r.permissions.includes(APP_CONFIG.PERMISSIONS.ALL)) return true;
    return r.permissions.includes(canonical);
  }
  
  // ================================
  // Exposición global (congelada)
  // ================================
  window.APP_CONFIG = APP_CONFIG;
  window.getEndpoint = getEndpoint;
  window.apiPath = apiPath;
  window.buildFetchInit = buildFetchInit;
  
  window.getRoleInfo = getRoleInfo;
  window.getRoleDisplayName = getRoleDisplayName;
  window.getRoleLevel = getRoleLevel;
  window.isRoleSuperiorOrEqual = isRoleSuperiorOrEqual;
  window.hasRolePermission = hasRolePermission;
  