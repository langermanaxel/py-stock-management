from app import db, create_app
from app.models.category import Category

def init_categories():
    app = create_app()
    with app.app_context():
        categories = [
            'the_ideal_coffee_for_you',
            'breakfasts_and_snacks',
            'toasted_sandwiches',
            'pastry_&_temptations',
            'drinks'
        ]
        for category in categories:
            if not Category.query.filter_by(name=category).first():
                category_obj = Category(name=category)
                db.session.add(category_obj)
        db.session.commit()

if __name__ == '__main__':
    init_categories()