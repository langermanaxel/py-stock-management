#!/usr/bin/env python3
"""
Script para verificar que los datos de ejemplo se hayan cargado correctamente en la base de datos.
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.database import db
from app.models.category import Category
from app.models.product import Product
from app.models.stock import Stock

def verify_data():
    """Verifica que los datos se hayan cargado correctamente"""
    
    print("🔍 Verificando datos en la base de datos...")
    print("=" * 60)
    
    # Crear la aplicación Flask
    app = create_app()
    
    with app.app_context():
        try:
            # Verificar categorías
            categories = Category.query.all()
            print(f"📂 Categorías encontradas: {len(categories)}")
            for category in categories:
                print(f"   - {category.name}")
            
            print()
            
            # Verificar productos
            products = Product.query.all()
            print(f"📦 Productos encontrados: {len(products)}")
            
            # Agrupar productos por categoría
            products_by_category = {}
            for product in products:
                category_name = product.category.name if product.category else "Sin categoría"
                if category_name not in products_by_category:
                    products_by_category[category_name] = []
                products_by_category[category_name].append(product)
            
            for category_name, category_products in products_by_category.items():
                print(f"   {category_name}: {len(category_products)} productos")
                for product in category_products[:3]:  # Mostrar solo los primeros 3
                    print(f"     • {product.name} - ${product.price}")
                if len(category_products) > 3:
                    print(f"     ... y {len(category_products) - 3} más")
            
            print()
            
            # Verificar stock
            stock_records = Stock.query.all()
            print(f"🏪 Registros de stock: {len(stock_records)}")
            
            # Verificar productos con bajo stock
            low_stock_products = []
            for stock in stock_records:
                if stock.quantity <= stock.min_stock:
                    product = Product.query.get(stock.product_id)
                    if product:
                        low_stock_products.append({
                            'product': product.name,
                            'current': stock.quantity,
                            'min': stock.min_stock
                        })
            
            if low_stock_products:
                print(f"⚠️  Productos con bajo stock: {len(low_stock_products)}")
                for item in low_stock_products:
                    print(f"   • {item['product']}: {item['current']}/{item['min']}")
            else:
                print("✅ Todos los productos tienen stock suficiente")
            
            print()
            
            # Estadísticas generales
            total_value = sum(product.price * stock.quantity for product in products 
                            for stock in stock_records if stock.product_id == product.id)
            
            print("📊 Estadísticas Generales:")
            print(f"   - Valor total del inventario: ${total_value:,.2f}")
            print(f"   - Precio promedio por producto: ${sum(p.price for p in products) / len(products):.2f}")
            print(f"   - Stock total: {sum(s.quantity for s in stock_records)} unidades")
            
            print("\n🎉 ¡Verificación completada exitosamente!")
            
        except Exception as e:
            print(f"❌ Error verificando datos: {e}")
            raise

if __name__ == "__main__":
    verify_data() 