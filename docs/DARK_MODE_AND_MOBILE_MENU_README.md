# Modo Oscuro y Menú Hamburguesa - Stock Management System

## Descripción General

Se han implementado dos nuevas características importantes para mejorar la experiencia del usuario:

1. **Modo Oscuro**: Permite cambiar entre tema claro y oscuro
2. **Menú Hamburguesa**: Navegación responsive para dispositivos móviles y tablets

## Características Implementadas

### 🌙 Modo Oscuro

#### Funcionalidades
- **Toggle de tema**: Botón para cambiar entre modo claro y oscuro
- **Persistencia**: El tema seleccionado se guarda en localStorage
- **Aplicación automática**: El tema se aplica automáticamente al cargar la página
- **Transiciones suaves**: Cambios de tema con animaciones fluidas

#### Implementación Técnica
- **Archivo**: `static/js/theme.js`
- **Clase**: `ThemeManager`
- **Almacenamiento**: `localStorage` con clave `theme`
- **Eventos**: Dispara evento personalizado `themeChanged` para otros componentes

#### Estilos del Modo Oscuro
- **Colores de fondo**: Cambio de blanco a gris oscuro
- **Texto**: Adaptación de colores para mejor contraste
- **Sombras**: Ajuste de opacidad para el modo oscuro
- **Bordes**: Adaptación de colores de borde

### 📱 Menú Hamburguesa

#### Funcionalidades
- **Botón hamburguesa**: Visible solo en dispositivos móviles (< 768px)
- **Menú deslizante**: Se desliza desde la izquierda
- **Overlay**: Fondo oscuro semi-transparente
- **Cierre automático**: Se cierra al hacer clic en elementos del menú
- **Responsive**: Se adapta automáticamente al tamaño de pantalla

#### Implementación Técnica
- **Archivo**: `static/js/mobile-menu.js`
- **Clase**: `MobileMenuManager`
- **Estado**: Controla apertura/cierre del menú
- **Eventos**: Maneja clics, resize de ventana y navegación

#### Características del Menú
- **Ancho**: 280px (máximo 80% del viewport)
- **Posición**: Fixed, se superpone al contenido
- **Z-index**: 50 (por encima del overlay)
- **Transiciones**: Animaciones suaves de entrada/salida

## Archivos Modificados

### Nuevos Archivos Creados
1. **`static/js/theme.js`** - Sistema de gestión de temas
2. **`static/js/mobile-menu.js`** - Sistema de menú móvil

### Archivos CSS Actualizados
1. **`static/css/style.css`** - Agregados estilos para modo oscuro y menú móvil

### Plantillas HTML Actualizadas
1. **`templates/users.html`** - Usuarios con modo oscuro y menú móvil
2. **`templates/dashboard.html`** - Dashboard con modo oscuro y menú móvil
3. **`templates/categories.html`** - Categorías con modo oscuro y menú móvil
4. **`templates/purchases.html`** - Compras con modo oscuro y menú móvil

## Estructura de Implementación

### Navegación Principal
```html
<!-- Botón de menú móvil -->
<div class="md:hidden">
    <button id="mobile-menu-button" class="mobile-menu-button">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
        </svg>
    </button>
</div>

<!-- Botón de cambio de tema -->
<button id="theme-toggle" class="theme-toggle">
    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <!-- Icono de luna/sol -->
    </svg>
</button>
```

### Menú Móvil
```html
<!-- Overlay del menú -->
<div id="mobile-menu-overlay" class="mobile-menu-overlay hidden"></div>

<!-- Menú deslizante -->
<div id="mobile-menu" class="mobile-menu">
    <div class="mobile-menu-header">
        <h3>Menú</h3>
        <button class="mobile-menu-close">×</button>
    </div>
    <nav class="mobile-menu-nav">
        <!-- Enlaces de navegación -->
    </nav>
</div>
```

## Clases CSS Principales

### Modo Oscuro
- `.dark-mode` - Clase principal para activar modo oscuro
- `.dark-mode .bg-white` - Fondo oscuro para elementos blancos
- `.dark-mode .text-gray-700` - Texto claro para modo oscuro

### Menú Móvil
- `.mobile-menu` - Contenedor principal del menú
- `.mobile-menu-overlay` - Fondo oscuro semi-transparente
- `.mobile-menu-item` - Elementos individuales del menú
- `.mobile-menu-button` - Botón hamburguesa
- `.theme-toggle` - Botón de cambio de tema

## Uso y Configuración

### Inicialización Automática
```javascript
// Se ejecuta automáticamente al cargar la página
x-init="initTheme()"

// Función en Alpine.js
initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
    }
}
```

### Cambio de Tema
```javascript
// Cambiar tema manualmente
themeManager.toggleTheme();

// Obtener tema actual
const currentTheme = themeManager.getCurrentTheme();
```

### Control del Menú Móvil
```javascript
// Abrir menú
mobileMenuManager.openMobileMenu();

// Cerrar menú
mobileMenuManager.closeMobileMenu();

// Verificar estado
const isOpen = mobileMenuManager.isMobileMenuOpen();
```

## Responsive Design

### Breakpoints
- **Mobile**: < 640px - Menú hamburguesa visible
- **Tablet**: 640px - 768px - Menú hamburguesa visible
- **Desktop**: > 768px - Navegación horizontal visible

### Clases Responsive
- `.md:hidden` - Ocultar en desktop
- `.mobile-only` - Mostrar solo en móvil
- `.desktop-only` - Mostrar solo en desktop

## Personalización

### Colores del Modo Oscuro
```css
.dark-mode {
    background-color: #111827; /* Gris muy oscuro */
    color: #f9fafb; /* Blanco */
}

.dark-mode .bg-white {
    background-color: #1f2937; /* Gris oscuro */
}
```

### Estilos del Menú Móvil
```css
.mobile-menu {
    width: 280px;
    max-width: 80vw;
    background-color: white;
    transform: translateX(-100%);
    transition: transform 0.3s ease-in-out;
}
```

## Compatibilidad

### Navegadores Soportados
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

### Características Requeridas
- CSS Grid y Flexbox
- CSS Transitions
- localStorage API
- ES6 Classes

## Mantenimiento

### Agregar Nuevas Plantillas
Para agregar modo oscuro y menú móvil a nuevas plantillas:

1. **Incluir scripts**:
```html
<script src="{{ url_for('static', filename='js/theme.js') }}" defer></script>
<script src="{{ url_for('static', filename='js/mobile-menu.js') }}" defer></script>
```

2. **Inicializar tema**:
```html
<body x-data="app()" x-init="initTheme()">
```

3. **Agregar botón de tema**:
```html
<button id="theme-toggle" class="theme-toggle">
    <!-- Icono de luna/sol -->
</button>
```

4. **Agregar menú móvil**:
```html
<!-- Botón hamburguesa -->
<div class="md:hidden">
    <button id="mobile-menu-button" class="mobile-menu-button">
        <!-- Icono hamburguesa -->
    </button>
</div>

<!-- Menú deslizante -->
<div id="mobile-menu" class="mobile-menu">
    <!-- Contenido del menú -->
</div>
```

### Actualizar Estilos
Para agregar nuevos estilos de modo oscuro:

```css
.dark-mode .nueva-clase {
    /* Estilos para modo oscuro */
    background-color: #1f2937;
    color: #f9fafb;
}
```

## Troubleshooting

### Problemas Comunes

1. **El tema no se guarda**
   - Verificar que localStorage esté habilitado
   - Revisar consola del navegador para errores

2. **El menú móvil no funciona**
   - Verificar que los IDs coincidan
   - Asegurar que los scripts se carguen correctamente

3. **Estilos no se aplican**
   - Verificar que las clases CSS estén definidas
   - Comprobar que no haya conflictos con otros estilos

### Debug
```javascript
// Verificar tema actual
console.log('Tema actual:', themeManager.getCurrentTheme());

// Verificar estado del menú
console.log('Menú abierto:', mobileMenuManager.isMobileMenuOpen());

// Verificar localStorage
console.log('Tema guardado:', localStorage.getItem('theme'));
```

## Futuras Mejoras

### Funcionalidades Planificadas
- **Tema automático**: Detectar preferencia del sistema
- **Más temas**: Temas personalizados adicionales
- **Animaciones**: Transiciones más elaboradas
- **Accesibilidad**: Mejoras para lectores de pantalla

### Optimizaciones
- **Lazy loading**: Cargar estilos solo cuando sea necesario
- **CSS Variables**: Usar variables CSS para mejor mantenimiento
- **Performance**: Optimizar transiciones y animaciones

## Conclusión

La implementación del modo oscuro y menú hamburguesa mejora significativamente la experiencia del usuario al:

- **Reducir la fatiga visual** con el modo oscuro
- **Mejorar la navegación** en dispositivos móviles
- **Mantener consistencia** en toda la aplicación
- **Proporcionar flexibilidad** en la personalización

Estas características están completamente integradas con el sistema existente y mantienen la compatibilidad con todos los navegadores modernos.
