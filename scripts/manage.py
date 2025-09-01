#!/usr/bin/env python3
"""
Sistema de Gestión Unificado para Stock Management
================================================

Este script proporciona una interfaz CLI unificada para todas las operaciones
de gestión de datos, migración y mantenimiento de la aplicación.

Uso:
    python manage.py --help                    # Ver ayuda general
    python manage.py seed --help               # Ver ayuda de seeding
    python manage.py seed --demo               # Cargar datos de demostración
    python manage.py seed --custom             # Cargar productos personalizados
    python manage.py seed --all                # Cargar todos los datos
    python manage.py db --help                 # Ver ayuda de base de datos
    python manage.py db init                   # Inicializar base de datos
    python manage.py db migrate                # Crear migración
    python manage.py db upgrade                # Aplicar migraciones
    python manage.py user --help               # Ver ayuda de usuarios
    python manage.py user create-admin         # Crear usuario administrador
    python manage.py user create-sample        # Crear usuarios de muestra
"""

import os
import sys
import click
from pathlib import Path

# Agregar el directorio raíz al path para importar la app
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Importar solo lo necesario para el CLI
try:
    from app import create_app, db
    from app.models import User, Category, Product, Stock, Order, OrderItem, PurchaseOrder, PurchaseOrderItem
    FLASK_AVAILABLE = True
except ImportError as e:
    click.echo(f"⚠️  Advertencia: No se pudo importar Flask app: {e}")
    click.echo("   Algunos comandos pueden no funcionar correctamente")
    FLASK_AVAILABLE = False


@click.group()
@click.version_option(version="1.0.0", prog_name="Stock Management CLI")
@click.option('--config', default='development', help='Configuración a usar (development/production)')
@click.pass_context
def cli(ctx, config):
    """Sistema de Gestión Unificado para Stock Management"""
    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    
    if FLASK_AVAILABLE:
        # Configurar Flask app
        os.environ['FLASK_ENV'] = config
        try:
            ctx.obj['app'] = create_app()
            ctx.obj['db'] = db
        except Exception as e:
            click.echo(f"⚠️  Advertencia: Error al inicializar Flask app: {e}")
            ctx.obj['app'] = None
            ctx.obj['db'] = None
    else:
        ctx.obj['app'] = None
        ctx.obj['db'] = None


@cli.group()
@click.pass_context
def seed(ctx):
    """Operaciones de seeding de datos"""
    if not ctx.obj.get('app'):
        click.echo("❌ Error: Flask app no disponible")
        sys.exit(1)
    pass


@seed.command()
@click.option('--force', is_flag=True, help='Forzar recreación de datos existentes')
@click.pass_context
def demo(ctx, force):
    """Cargar datos de demostración completos"""
    app = ctx.obj['app']
    
    with app.app_context():
        click.echo("🌱 Cargando datos de demostración...")
        
        try:
            # Crear categorías
            categories_data = [
                {"name": "Electrónicos", "description": "Productos electrónicos y tecnología"},
                {"name": "Ropa", "description": "Vestimenta y accesorios"},
                {"name": "Hogar", "description": "Artículos para el hogar"},
                {"name": "Deportes", "description": "Equipamiento deportivo"},
                {"name": "Libros", "description": "Libros y material educativo"}
            ]
            
            for cat_data in categories_data:
                category = Category.query.filter_by(name=cat_data["name"]).first()
                if not category:
                    category = Category(**cat_data)
                    db.session.add(category)
                    click.echo(f"  ✅ Categoría creada: {cat_data['name']}")
                else:
                    click.echo(f"  ℹ️  Categoría existente: {cat_data['name']}")
            
            db.session.commit()
            
            # Crear productos
            products_data = [
                {"name": "Laptop HP", "description": "Laptop HP Pavilion 15", "category_id": 1, "price": 899.99},
                {"name": "Smartphone Samsung", "description": "Samsung Galaxy S21", "category_id": 1, "price": 699.99},
                {"name": "Camiseta Básica", "description": "Camiseta de algodón 100%", "category_id": 2, "price": 19.99},
                {"name": "Jeans Clásicos", "description": "Jeans azules de alta calidad", "category_id": 2, "price": 49.99},
                {"name": "Sofá 3 Plazas", "description": "Sofá moderno y cómodo", "category_id": 3, "price": 599.99},
                {"name": "Mesa de Centro", "description": "Mesa de centro de madera", "category_id": 3, "price": 129.99},
                {"name": "Pelota de Fútbol", "description": "Pelota oficial FIFA", "category_id": 4, "price": 29.99},
                {"name": "Raqueta de Tenis", "description": "Raqueta profesional Wilson", "category_id": 4, "price": 89.99},
                {"name": "Python para Principiantes", "description": "Libro de Python básico", "category_id": 5, "price": 24.99},
                {"name": "Historia del Arte", "description": "Compendio de historia del arte", "category_id": 5, "price": 34.99}
            ]
            
            for prod_data in products_data:
                product = Product.query.filter_by(name=prod_data["name"]).first()
                if not product:
                    product = Product(**prod_data)
                    db.session.add(product)
                    click.echo(f"  ✅ Producto creado: {prod_data['name']}")
                else:
                    click.echo(f"  ℹ️  Producto existente: {prod_data['name']}")
            
            db.session.commit()
            
            # Crear stock inicial
            for product in Product.query.all():
                stock = Stock.query.filter_by(product_id=product.id).first()
                if not stock:
                    initial_quantity = 50 if product.category_id == 1 else 100  # Más stock para ropa
                    stock = Stock(
                        product_id=product.id,
                        quantity=initial_quantity,
                        min_stock=10,
                        location="Almacén Principal"
                    )
                    db.session.add(stock)
                    click.echo(f"  ✅ Stock creado: {product.name} - {initial_quantity} unidades")
                else:
                    click.echo(f"  ℹ️  Stock existente: {product.name} - {stock.quantity} unidades")
            
            db.session.commit()
            
            click.echo("🎉 Datos de demostración cargados exitosamente!")
            
        except Exception as e:
            click.echo(f"❌ Error al cargar datos: {e}")
            db.session.rollback()
            sys.exit(1)


@seed.command()
@click.option('--force', is_flag=True, help='Forzar recreación de productos personalizados')
@click.pass_context
def custom(ctx, force):
    """Cargar productos personalizados adicionales"""
    app = ctx.obj['app']
    
    with app.app_context():
        click.echo("🎨 Cargando productos personalizados...")
        
        try:
            # Productos personalizados adicionales
            custom_products = [
                {"name": "Auriculares Bluetooth", "description": "Auriculares inalámbricos premium", "category_id": 1, "price": 79.99},
                {"name": "Reloj Inteligente", "description": "Smartwatch con monitor cardíaco", "category_id": 1, "price": 199.99},
                {"name": "Zapatillas Running", "description": "Zapatillas para correr profesionales", "category_id": 4, "price": 119.99},
                {"name": "Mochila Escolar", "description": "Mochila resistente para estudiantes", "category_id": 3, "price": 39.99},
                {"name": "Cafetera Express", "description": "Cafetera automática profesional", "category_id": 3, "price": 299.99}
            ]
            
            for prod_data in custom_products:
                product = Product.query.filter_by(name=prod_data["name"]).first()
                if not product:
                    product = Product(**prod_data)
                    db.session.add(product)
                    click.echo(f"  ✅ Producto personalizado creado: {prod_data['name']}")
                    
                    # Crear stock para el producto
                    stock = Stock(
                        product_id=product.id,
                        quantity=25,
                        min_stock=5,
                        location="Almacén Secundario"
                    )
                    db.session.add(stock)
                else:
                    click.echo(f"  ℹ️  Producto personalizado existente: {prod_data['name']}")
            
            db.session.commit()
            click.echo("🎉 Productos personalizados cargados exitosamente!")
            
        except Exception as e:
            click.echo(f"❌ Error al cargar productos personalizados: {e}")
            db.session.rollback()
            sys.exit(1)


@seed.command()
@click.option('--force', is_flag=True, help='Forzar recreación de todos los datos')
@click.pass_context
def all(ctx, force):
    """Cargar todos los datos (demo + personalizados)"""
    click.echo("🚀 Cargando todos los datos...")
    
    # Ejecutar demo primero
    ctx.invoke(demo, force=force)
    
    # Luego ejecutar custom
    ctx.invoke(custom, force=force)
    
    click.echo("🎉 Todos los datos han sido cargados exitosamente!")


@cli.group()
@click.pass_context
def db(ctx):
    """Operaciones de base de datos"""
    if not ctx.obj.get('app'):
        click.echo("❌ Error: Flask app no disponible")
        sys.exit(1)
    pass


@db.command()
@click.pass_context
def init(ctx):
    """Inicializar base de datos"""
    app = ctx.obj['app']
    
    with app.app_context():
        click.echo("🗄️  Inicializando base de datos...")
        
        try:
            # Crear todas las tablas
            db.create_all()
            click.echo("✅ Base de datos inicializada exitosamente!")
            
        except Exception as e:
            click.echo(f"❌ Error al inicializar base de datos: {e}")
            sys.exit(1)


@db.command()
@click.pass_context
def migrate(ctx):
    """Crear nueva migración"""
    app = ctx.obj['app']
    
    with app.app_context():
        click.echo("🔄 Creando migración...")
        
        try:
            # Aquí se ejecutaría flask db migrate
            click.echo("⚠️  Función de migración requiere Flask-Migrate configurado")
            click.echo("   Ejecuta manualmente: flask db migrate -m 'Descripción'")
            
        except Exception as e:
            click.echo(f"❌ Error al crear migración: {e}")
            sys.exit(1)


@db.command()
@click.pass_context
def upgrade(ctx):
    """Aplicar migraciones pendientes"""
    app = ctx.obj['app']
    
    with app.app_context():
        click.echo("⬆️  Aplicando migraciones...")
        
        try:
            # Aquí se ejecutaría flask db upgrade
            click.echo("⚠️  Función de upgrade requiere Flask-Migrate configurado")
            click.echo("   Ejecuta manualmente: flask db upgrade")
            
        except Exception as e:
            click.echo(f"❌ Error al aplicar migraciones: {e}")
            sys.exit(1)


@cli.group()
@click.pass_context
def user(ctx):
    """Operaciones de usuarios"""
    if not ctx.obj.get('app'):
        click.echo("❌ Error: Flask app no disponible")
        sys.exit(1)
    pass


@user.command()
@click.option('--username', prompt='Nombre de usuario', help='Nombre de usuario del administrador')
@click.option('--email', prompt='Email', help='Email del administrador')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Contraseña del administrador')
@click.option('--first-name', prompt='Nombre', help='Nombre del administrador')
@click.option('--last-name', prompt='Apellido', help='Apellido del administrador')
@click.pass_context
def create_admin(ctx, username, email, password, first_name, last_name):
    """Crear usuario administrador"""
    app = ctx.obj['app']
    
    with app.app_context():
        click.echo("👑 Creando usuario administrador...")
        
        try:
            # Verificar si ya existe
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                click.echo(f"⚠️  El usuario '{username}' ya existe")
                if click.confirm("¿Deseas actualizar el rol a administrador?"):
                    existing_user.role = 'admin'
                    db.session.commit()
                    click.echo("✅ Rol actualizado a administrador")
                return
            
            # Crear nuevo usuario administrador
            admin_user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role='admin',
                is_active=True
            )
            admin_user.set_password(password)
            
            db.session.add(admin_user)
            db.session.commit()
            
            click.echo(f"✅ Usuario administrador '{username}' creado exitosamente!")
            
        except Exception as e:
            click.echo(f"❌ Error al crear usuario administrador: {e}")
            db.session.rollback()
            sys.exit(1)


@user.command()
@click.pass_context
def create_sample(ctx):
    """Crear usuarios de muestra"""
    app = ctx.obj['app']
    
    with app.app_context():
        click.echo("👥 Creando usuarios de muestra...")
        
        try:
            sample_users = [
                {
                    "username": "manager1",
                    "email": "manager1@example.com",
                    "password": "manager123",
                    "first_name": "Ana",
                    "last_name": "García",
                    "role": "manager"
                },
                {
                    "username": "user1",
                    "email": "user1@example.com",
                    "password": "user123",
                    "first_name": "Carlos",
                    "last_name": "López",
                    "role": "user"
                },
                {
                    "username": "viewer1",
                    "email": "viewer1@example.com",
                    "password": "viewer123",
                    "first_name": "María",
                    "last_name": "Rodríguez",
                    "role": "viewer"
                }
            ]
            
            for user_data in sample_users:
                existing_user = User.query.filter_by(username=user_data["username"]).first()
                if not existing_user:
                    user = User(
                        username=user_data["username"],
                        email=user_data["email"],
                        first_name=user_data["first_name"],
                        last_name=user_data["last_name"],
                        role=user_data["role"],
                        is_active=True
                    )
                    user.set_password(user_data["password"])
                    
                    db.session.add(user)
                    click.echo(f"  ✅ Usuario creado: {user_data['username']} ({user_data['role']})")
                else:
                    click.echo(f"  ℹ️  Usuario existente: {user_data['username']}")
            
            db.session.commit()
            click.echo("🎉 Usuarios de muestra creados exitosamente!")
            
        except Exception as e:
            click.echo(f"❌ Error al crear usuarios de muestra: {e}")
            db.session.rollback()
            sys.exit(1)


@cli.command()
@click.pass_context
def status(ctx):
    """Mostrar estado actual de la aplicación"""
    if not ctx.obj.get('app'):
        click.echo("❌ Error: Flask app no disponible")
        sys.exit(1)
    
    app = ctx.obj['app']
    
    with app.app_context():
        click.echo("📊 Estado de la aplicación:")
        click.echo("=" * 40)
        
        try:
            # Contar registros
            categories_count = Category.query.count()
            products_count = Product.query.count()
            stock_count = Stock.query.count()
            users_count = User.query.count()
            orders_count = Order.query.count()
            purchase_orders_count = PurchaseOrder.query.count()
            
            click.echo(f"📁 Categorías: {categories_count}")
            click.echo(f"📦 Productos: {products_count}")
            click.echo(f"📊 Stock: {stock_count}")
            click.echo(f"👥 Usuarios: {users_count}")
            click.echo(f"🛒 Órdenes de venta: {orders_count}")
            click.echo(f"📋 Órdenes de compra: {purchase_orders_count}")
            
            # Verificar base de datos
            db.engine.execute("SELECT 1")
            click.echo("🗄️  Base de datos: ✅ Conectada")
            
            # Verificar configuración
            config = app.config
            click.echo(f"⚙️  Entorno: {config.get('FLASK_ENV', 'development')}")
            click.echo(f"🔐 JWT habilitado: {'✅' if hasattr(app, 'jwt') else '❌'}")
            click.echo(f"📚 API docs: {'✅' if hasattr(app, 'api') else '❌'}")
            
        except Exception as e:
            click.echo(f"❌ Error al obtener estado: {e}")


@cli.command()
@click.pass_context
def shell(ctx):
    """Abrir shell interactivo de Flask"""
    if not ctx.obj.get('app'):
        click.echo("❌ Error: Flask app no disponible")
        sys.exit(1)
    
    app = ctx.obj['app']
    
    with app.app_context():
        click.echo("🐍 Abriendo shell interactivo...")
        click.echo("   Variables disponibles: app, db, User, Category, Product, Stock, Order, PurchaseOrder")
        
        try:
            import code
            code.interact(local=locals())
        except KeyboardInterrupt:
            click.echo("\n👋 Shell cerrado")


if __name__ == '__main__':
    cli()
