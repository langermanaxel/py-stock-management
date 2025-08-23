"""
Validaciones de Negocio - Sistema de Gestión de Inventario
Implementa reglas críticas de negocio para mantener integridad de datos
"""

from typing import List, Dict, Any, Tuple
from flask import current_app
from ..database import db
from ..models.stock import Stock
from ..models.order import Order
from ..models.order_item import OrderItem
from ..models.product import Product


class BusinessRuleViolation(Exception):
    """Excepción para violaciones de reglas de negocio"""
    def __init__(self, message: str, field: str = None, value: Any = None):
        self.message = message
        self.field = field
        self.value = value
        super().__init__(self.message)


class StockValidator:
    """Validador de reglas de negocio para stock"""
    
    @staticmethod
    def validate_quantity(quantity: int, field: str = "quantity") -> None:
        """Valida que la cantidad sea positiva"""
        if not isinstance(quantity, int) or quantity < 0:
            raise BusinessRuleViolation(
                f"La cantidad debe ser un número entero positivo, recibido: {quantity}",
                field, quantity
            )
    
    @staticmethod
    def validate_min_stock(min_stock: int, field: str = "min_stock") -> None:
        """Valida que el stock mínimo sea no-negativo"""
        if not isinstance(min_stock, int) or min_stock < 0:
            raise BusinessRuleViolation(
                f"El stock mínimo debe ser un número entero no-negativo, recibido: {min_stock}",
                field, min_stock
            )
    
    @staticmethod
    def validate_stock_update(product_id: int, new_quantity: int) -> None:
        """Valida que la actualización de stock no resulte en cantidad negativa"""
        StockValidator.validate_quantity(new_quantity, "quantity")
        
        # Verificar que no se vaya a stock negativo
        if new_quantity < 0:
            raise BusinessRuleViolation(
                f"No se puede establecer stock negativo para el producto {product_id}",
                "quantity", new_quantity
            )
    
    @staticmethod
    def check_stock_availability(product_id: int, requested_quantity: int) -> Tuple[bool, int]:
        """
        Verifica disponibilidad de stock para un producto
        
        Returns:
            Tuple[bool, int]: (disponible, stock_actual)
        """
        stock = Stock.query.filter_by(product_id=product_id).first()
        if not stock:
            raise BusinessRuleViolation(
                f"Producto {product_id} no tiene registro de stock",
                "product_id", product_id
            )
        
        available = stock.quantity >= requested_quantity
        return available, stock.quantity


class OrderValidator:
    """Validador de reglas de negocio para órdenes"""
    
    @staticmethod
    def validate_order_items(items: List[Dict[str, Any]]) -> None:
        """Valida la estructura y contenido de los items de la orden"""
        if not items or not isinstance(items, list):
            raise BusinessRuleViolation("La orden debe contener al menos un item")
        
        for i, item in enumerate(items):
            if not isinstance(item, dict):
                raise BusinessRuleViolation(f"Item {i} debe ser un diccionario")
            
            # Validar campos requeridos
            required_fields = ['product_id', 'quantity']
            for field in required_fields:
                if field not in item:
                    raise BusinessRuleViolation(f"Campo requerido '{field}' faltante en item {i}")
            
            # Validar tipos de datos
            if not isinstance(item['product_id'], int) or item['product_id'] <= 0:
                raise BusinessRuleViolation(
                    f"product_id debe ser un entero positivo en item {i}",
                    "product_id", item['product_id']
                )
            
            if not isinstance(item['quantity'], int) or item['quantity'] <= 0:
                raise BusinessRuleViolation(
                    f"quantity debe ser un entero positivo en item {i}",
                    "quantity", item['quantity']
                )
    
    @staticmethod
    def validate_order_creation(items: List[Dict[str, Any]]) -> None:
        """Valida que se pueda crear una orden con los items especificados"""
        OrderValidator.validate_order_items(items)
        
        # Verificar disponibilidad de stock para todos los items
        for item in items:
            product_id = item['product_id']
            quantity = item['quantity']
            
            # Verificar que el producto existe
            product = Product.query.get(product_id)
            if not product:
                raise BusinessRuleViolation(
                    f"Producto {product_id} no existe",
                    "product_id", product_id
                )
            
            # Verificar disponibilidad de stock
            available, current_stock = StockValidator.check_stock_availability(product_id, quantity)
            if not available:
                raise BusinessRuleViolation(
                    f"Stock insuficiente para producto {product_id}. "
                    f"Solicitado: {quantity}, Disponible: {current_stock}",
                    "quantity", quantity
                )
    
    @staticmethod
    def validate_order_completion(order_id: int) -> Tuple[Order, List[Tuple[Stock, int]]]:
        """
        Valida que se pueda completar una orden
        
        Returns:
            Tuple[Order, List[Tuple[Stock, int]]]: (orden, lista de (stock, cantidad_a_descontar))
        """
        order = Order.query.get(order_id)
        if not order:
            raise BusinessRuleViolation(f"Orden {order_id} no existe")
        
        if order.status != 'pending':
            raise BusinessRuleViolation(
                f"Solo se pueden completar órdenes pendientes. Estado actual: {order.status}",
                "status", order.status
            )
        
        if not order.items:
            raise BusinessRuleViolation("La orden no tiene items para procesar")
        
        # Verificar stock disponible para completar la orden
        stock_updates = []
        for item in order.items:
            stock = Stock.query.filter_by(product_id=item.product_id).first()
            if not stock:
                raise BusinessRuleViolation(
                    f"Producto {item.product_id} no tiene registro de stock"
                )
            
            # Verificar que hay suficiente stock
            if stock.quantity < item.quantity:
                raise BusinessRuleViolation(
                    f"Stock insuficiente para completar orden. "
                    f"Producto {item.product_id}: solicitado {item.quantity}, disponible {stock.quantity}"
                )
            
            stock_updates.append((stock, item.quantity))
        
        return order, stock_updates


class TransactionManager:
    """Gestor de transacciones para operaciones críticas"""
    
    @staticmethod
    def execute_order_completion(order_id: int) -> Dict[str, Any]:
        """
        Ejecuta la completación de una orden como transacción atómica
        
        Returns:
            Dict[str, Any]: Resultado de la operación
        """
        # Iniciar transacción
        db.session.begin_nested()
        
        try:
            # Validar que se puede completar la orden
            order, stock_updates = OrderValidator.validate_order_completion(order_id)
            
            # Aplicar descuentos de stock
            for stock, quantity_to_deduct in stock_updates:
                new_quantity = stock.quantity - quantity_to_deduct
                
                # Validar que no resulte en stock negativo
                if new_quantity < 0:
                    raise BusinessRuleViolation(
                        f"Operación resultaría en stock negativo para producto {stock.product_id}"
                    )
                
                stock.quantity = new_quantity
            
            # Marcar orden como completada
            order.status = 'completed'
            
            # Commit de la transacción anidada
            db.session.commit()
            
            # Commit de la transacción principal
            db.session.commit()
            
            return {
                'success': True,
                'message': f'Orden {order_id} completada exitosamente',
                'order': order.to_dict(),
                'stock_updated': len(stock_updates)
            }
            
        except Exception as e:
            # Rollback de la transacción anidada
            db.session.rollback()
            # Rollback de la transacción principal
            db.session.rollback()
            
            # Re-lanzar la excepción
            raise e
    
    @staticmethod
    def execute_stock_update(product_id: int, new_quantity: int, new_min_stock: int = None) -> Dict[str, Any]:
        """
        Ejecuta la actualización de stock como transacción atómica
        
        Returns:
            Dict[str, Any]: Resultado de la operación
        """
        # Iniciar transacción
        db.session.begin_nested()
        
        try:
            # Validar parámetros
            StockValidator.validate_stock_update(product_id, new_quantity)
            if new_min_stock is not None:
                StockValidator.validate_min_stock(new_min_stock)
            
            # Obtener stock actual
            stock = Stock.query.filter_by(product_id=product_id).first()
            if not stock:
                raise BusinessRuleViolation(f"Producto {product_id} no tiene registro de stock")
            
            # Actualizar stock
            old_quantity = stock.quantity
            stock.quantity = new_quantity
            
            if new_min_stock is not None:
                stock.min_stock = new_min_stock
            
            # Commit de la transacción anidada
            db.session.commit()
            
            # Commit de la transacción principal
            db.session.commit()
            
            return {
                'success': True,
                'message': f'Stock actualizado para producto {product_id}',
                'old_quantity': old_quantity,
                'new_quantity': new_quantity,
                'stock': stock.to_dict()
            }
            
        except Exception as e:
            # Rollback de la transacción anidada
            db.session.rollback()
            # Rollback de la transacción principal
            db.session.rollback()
            
            # Re-lanzar la excepción
            raise e


class BusinessRuleEngine:
    """Motor principal de validaciones de negocio"""
    
    @staticmethod
    def validate_all_business_rules() -> Dict[str, Any]:
        """Valida todas las reglas de negocio del sistema"""
        violations = []
        
        try:
            # Validar stock no-negativo
            negative_stocks = Stock.query.filter(Stock.quantity < 0).all()
            if negative_stocks:
                violations.append({
                    'rule': 'stock_no_negativo',
                    'message': f'Se encontraron {len(negative_stocks)} productos con stock negativo',
                    'details': [{'product_id': s.product_id, 'quantity': s.quantity} for s in negative_stocks]
                })
            
            # Validar stock mínimo válido
            invalid_min_stocks = Stock.query.filter(Stock.min_stock < 0).all()
            if invalid_min_stocks:
                violations.append({
                    'rule': 'min_stock_valido',
                    'message': f'Se encontraron {len(invalid_min_stocks)} productos con stock mínimo inválido',
                    'details': [{'product_id': s.product_id, 'min_stock': s.min_stock} for s in invalid_min_stocks]
                })
            
            # Validar órdenes con items duplicados
            orders_with_duplicates = []
            for order in Order.query.filter_by(status='pending').all():
                product_ids = [item.product_id for item in order.items]
                if len(product_ids) != len(set(product_ids)):
                    orders_with_duplicates.append(order.id)
            
            if orders_with_duplicates:
                violations.append({
                    'rule': 'ordenes_sin_duplicados',
                    'message': f'Se encontraron {len(orders_with_duplicates)} órdenes con productos duplicados',
                    'details': {'order_ids': orders_with_duplicates}
                })
            
            return {
                'valid': len(violations) == 0,
                'violations': violations,
                'total_checks': 4
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e),
                'violations': violations
            }
