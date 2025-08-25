from ..database import db
from datetime import datetime, timezone

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(200), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    total = db.Column(db.Numeric(10, 2), default=0)
    status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime)
    
    # Relaciones
    items = db.relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # created_by = db.relationship('User', back_populates='orders_created')

    def to_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'total': float(self.total) if self.total else 0,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'items': [item.to_dict() for item in self.items],
            'created_by': self.created_by.username if self.created_by else None
        }
