#!/usr/bin/env python3
"""
Script de demostración del sistema de notificaciones toast
"""

import webbrowser
import http.server
import socketserver
import threading
import time
import os
from pathlib import Path

def create_demo_html():
    """Crear archivo HTML de demostración"""
    demo_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Demo: Sistema de Notificaciones Toast</title>
    <link rel="stylesheet" href="static/css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
</head>
<body>
    <!-- Sistema de Notificaciones Toast -->
    <div id="toast-container" 
         x-data="toastManager()" 
         x-show="toasts.length > 0"
         class="toast-container">
        <template x-for="toast in toasts" :key="toast.id">
            <div x-show="toast.visible" 
                 x-transition:enter="toast-enter"
                 x-transition:enter-start="toast-enter-start"
                 x-transition:enter-end="toast-enter-end"
                 x-transition:leave="toast-leave"
                 x-transition:leave-start="toast-leave-start"
                 x-transition:leave-end="toast-leave-end"
                 :class="`toast toast-${toast.type}`"
                 @click="removeToast(toast.id)">
                <div class="toast-icon">
                    <i :class="getToastIcon(toast.type)"></i>
                </div>
                <div class="toast-content">
                    <div class="toast-title" x-text="toast.title"></div>
                    <div class="toast-message" x-text="toast.message"></div>
                </div>
                <button class="toast-close" @click="removeToast(toast.id)">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        </template>
    </div>

    <div class="container">
        <header class="header">
            <h1><i class="fas fa-bell"></i> Demo: Sistema de Notificaciones Toast</h1>
            <p>Demostración del sistema de notificaciones implementado con Alpine.js</p>
        </header>

        <main class="main">
            <div class="form-section">
                <h3>Prueba las Notificaciones</h3>
                
                <div class="form-group">
                    <label for="toastType">Tipo de Notificación:</label>
                    <select id="toastType" class="form-control">
                        <option value="success">✅ Éxito</option>
                        <option value="error">❌ Error</option>
                        <option value="warning">⚠️ Advertencia</option>
                        <option value="info">ℹ️ Información</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="toastTitle">Título:</label>
                    <input type="text" id="toastTitle" class="form-control" 
                           value="Notificación de Prueba" placeholder="Título de la notificación">
                </div>
                
                <div class="form-group">
                    <label for="toastMessage">Mensaje:</label>
                    <textarea id="toastMessage" class="form-control" rows="3" 
                              placeholder="Mensaje de la notificación">Esta es una notificación de demostración del sistema toast implementado con Alpine.js</textarea>
                </div>
                
                <div class="form-group">
                    <label for="toastDuration">Duración (ms):</label>
                    <input type="number" id="toastDuration" class="form-control" 
                           value="5000" min="1000" max="30000" step="1000">
                </div>
                
                <button type="button" onclick="showCustomToast()" class="btn btn-primary">
                    <i class="fas fa-bell"></i> Mostrar Notificación
                </button>
            </div>

            <div class="form-section">
                <h3>Notificaciones Automáticas</h3>
                
                <div class="form-row">
                    <button type="button" onclick="showSuccessToast()" class="btn btn-success">
                        <i class="fas fa-check"></i> Éxito
                    </button>
                    
                    <button type="button" onclick="showErrorToast()" class="btn btn-danger">
                        <i class="fas fa-times"></i> Error
                    </button>
                    
                    <button type="button" onclick="showWarningToast()" class="btn btn-warning">
                        <i class="fas fa-exclamation-triangle"></i> Advertencia
                    </button>
                    
                    <button type="button" onclick="showInfoToast()" class="btn btn-secondary">
                        <i class="fas fa-info-circle"></i> Información
                    </button>
                </div>
                
                <div class="form-row">
                    <button type="button" onclick="showMultipleToasts()" class="btn btn-primary">
                        <i class="fas fa-layer-group"></i> Múltiples Notificaciones
                    </button>
                    
                    <button type="button" onclick="clearAllToasts()" class="btn btn-danger">
                        <i class="fas fa-trash"></i> Limpiar Todas
                    </button>
                </div>
            </div>

            <div class="form-section">
                <h3>Características del Sistema</h3>
                
                <div class="dashboard-grid">
                    <div class="dashboard-card">
                        <h3>🎨 Diseño Moderno</h3>
                        <p>Interfaz limpia y profesional con animaciones suaves</p>
                    </div>
                    
                    <div class="dashboard-card">
                        <h3>📱 Responsivo</h3>
                        <p>Se adapta perfectamente a todos los dispositivos</p>
                    </div>
                    
                    <div class="dashboard-card">
                        <h3>⚡ Alpine.js</h3>
                        <p>Micro-framework ligero sin reescribir la aplicación</p>
                    </div>
                    
                    <div class="dashboard-card">
                        <h3>🔧 Fácil de Usar</h3>
                        <p>API simple y consistente para todas las notificaciones</p>
                    </div>
                </div>
            </div>

            <div class="form-section">
                <h3>Tipos de Notificaciones</h3>
                
                <div class="list-section">
                    <div class="list-item">
                        <div class="list-item-header">
                            <div class="list-item-title">✅ Éxito (Success)</div>
                            <span class="badge badge-success">Verde</span>
                        </div>
                        <p class="text-muted">Para operaciones exitosas, confirmaciones y mensajes positivos</p>
                    </div>
                    
                    <div class="list-item">
                        <div class="list-item-header">
                            <div class="list-item-title">❌ Error</div>
                            <span class="badge badge-danger">Rojo</span>
                        </div>
                        <p class="text-muted">Para errores, fallos y problemas que requieren atención</p>
                    </div>
                    
                    <div class="list-item">
                        <div class="list-item-header">
                            <div class="list-item-title">⚠️ Advertencia (Warning)</div>
                            <span class="badge badge-warning">Naranja</span>
                        </div>
                        <p class="text-muted">Para advertencias, precauciones y situaciones que requieren cuidado</p>
                    </div>
                    
                    <div class="list-item">
                        <div class="list-item-header">
                            <div class="list-item-title">ℹ️ Información (Info)</div>
                            <span class="badge badge-info">Azul</span>
                        </div>
                        <p class="text-muted">Para información general, tips y mensajes informativos</p>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script>
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

        // Funciones de demostración
        function showCustomToast() {
            const type = document.getElementById('toastType').value;
            const title = document.getElementById('toastTitle').value;
            const message = document.getElementById('toastMessage').value;
            const duration = parseInt(document.getElementById('toastDuration').value);
            
            if (!title.trim() || !message.trim()) {
                alert('Por favor completa título y mensaje');
                return;
            }
            
            // Usar Alpine.js si está disponible
            if (window.Alpine && window.Alpine.store && window.Alpine.store('toast')) {
                window.Alpine.store('toast').showToast(type, title, message, duration);
            } else {
                // Fallback
                alert(`${title}: ${message}`);
            }
        }

        function showSuccessToast() {
            if (window.Alpine && window.Alpine.store && window.Alpine.store('toast')) {
                window.Alpine.store('toast').success(
                    'Operación Exitosa', 
                    'La operación se completó correctamente', 
                    4000
                );
            }
        }

        function showErrorToast() {
            if (window.Alpine && window.Alpine.store && window.Alpine.store('toast')) {
                window.Alpine.store('toast').error(
                    'Error Detectado', 
                    'Ocurrió un error durante la operación', 
                    6000
                );
            }
        }

        function showWarningToast() {
            if (window.Alpine && window.Alpine.store && window.Alpine.store('toast')) {
                window.Alpine.store('toast').warning(
                    'Advertencia', 
                    'Esta acción puede tener consecuencias importantes', 
                    5000
                );
            }
        }

        function showInfoToast() {
            if (window.Alpine && window.Alpine.store && window.Alpine.store('toast')) {
                window.Alpine.store('toast').info(
                    'Información', 
                    'Este es un mensaje informativo del sistema', 
                    4000
                );
            }
        }

        function showMultipleToasts() {
            if (window.Alpine && window.Alpine.store && window.Alpine.store('toast')) {
                const store = window.Alpine.store('toast');
                
                store.success('Primera Notificación', 'Esta es la primera notificación', 3000);
                
                setTimeout(() => {
                    store.info('Segunda Notificación', 'Esta es la segunda notificación', 3000);
                }, 500);
                
                setTimeout(() => {
                    store.warning('Tercera Notificación', 'Esta es la tercera notificación', 3000);
                }, 1000);
                
                setTimeout(() => {
                    store.error('Cuarta Notificación', 'Esta es la cuarta notificación', 3000);
                }, 1500);
            }
        }

        function clearAllToasts() {
            if (window.Alpine && window.Alpine.store && window.Alpine.store('toast')) {
                const store = window.Alpine.store('toast');
                store.toasts = [];
            }
        }

        // Inicializar Alpine.js store
        document.addEventListener('DOMContentLoaded', function() {
            if (window.Alpine) {
                window.Alpine.store('toast', toastManager());
            }
        });
    </script>
</body>
</html>"""
    
    # Crear directorio si no existe
    demo_dir = Path("demo_toast")
    demo_dir.mkdir(exist_ok=True)
    
    # Crear archivo HTML
    demo_file = demo_dir / "index.html"
    with open(demo_file, 'w', encoding='utf-8') as f:
        f.write(demo_html)
    
    return demo_file

def start_demo_server(port=8000):
    """Iniciar servidor de demostración"""
    # Cambiar al directorio de demo
    demo_dir = Path("demo_toast")
    os.chdir(demo_dir)
    
    # Crear servidor HTTP simple
    handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"🚀 Servidor de demostración iniciado en http://localhost:{port}")
        print(f"📁 Sirviendo archivos desde: {demo_dir.absolute()}")
        print("🌐 Abriendo navegador automáticamente...")
        print("⏹️  Presiona Ctrl+C para detener el servidor")
        
        # Abrir navegador automáticamente
        webbrowser.open(f"http://localhost:{port}")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Servidor detenido")
            httpd.shutdown()

def main():
    """Función principal"""
    print("🎉 DEMO: Sistema de Notificaciones Toast")
    print("=" * 50)
    
    # Crear archivo de demostración
    demo_file = create_demo_html()
    print(f"✅ Archivo de demostración creado: {demo_file}")
    
    # Verificar que Alpine.js esté disponible
    print("🔍 Verificando Alpine.js...")
    try:
        import urllib.request
        response = urllib.request.urlopen("https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js")
        if response.status == 200:
            print("✅ Alpine.js está disponible")
        else:
            print("⚠️  Alpine.js podría no estar disponible")
    except:
        print("⚠️  No se pudo verificar Alpine.js")
    
    print("\n📋 Características del Sistema:")
    print("   🎨 Notificaciones toast modernas y responsivas")
    print("   ⚡ Implementado con Alpine.js (micro-framework)")
    print("   🎭 4 tipos de notificaciones: éxito, error, advertencia, info")
    print("   🔄 Auto-remoción configurable")
    print("   📱 Diseño completamente responsivo")
    print("   🎯 API simple y consistente")
    
    print("\n🚀 Iniciando servidor de demostración...")
    start_demo_server()

if __name__ == "__main__":
    main()
