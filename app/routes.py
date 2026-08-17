from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models import MenuItem, Order, OrderItem

main = Blueprint('main', __name__)

# Sample Data Add karne ke liye Helper Route
@main.route('/seed')
def seed_db():
    if MenuItem.query.count() == 0:
        items = [
            MenuItem(name="Paneer Butter Masala", price=250.0, description="Rich gravy paneer dish", category="Main Course"),
            MenuItem(name="Butter Naan", price=40.0, description="Fresh baked butter naan", category="Breads"),
            MenuItem(name="Veg Biryani", price=200.0, description="Aromatic rice with spices", category="Main Course"),
            MenuItem(name="Gulab Jamun", price=60.0, description="2 pcs warm sweet dessert", category="Desserts")
        ]
        db.session.add_all(items)
        db.session.commit()
        return jsonify({"message": "Database Seeded Successfully!"})
    return jsonify({"message": "Database already has data."})

# 1. Home / Menu Page
@main.route('/')
def index():
    menu_items = MenuItem.query.all()
    return render_template('index.html', menu_items=menu_items)

# 2. Cart Page
@main.route('/cart')
def cart():
    return render_template('cart.html')

# 3. Order Processing API Endpoint
@main.route('/api/order', methods=['POST'])
def create_order():
    data = request.get_json()
    
    cart_items = data.get('cart', [])
    user_id = data.get('user_id', 0)
    user_name = data.get('user_name', 'Guest')
    
    if not cart_items:
        return jsonify({"success": False, "message": "Cart is empty"}), 400

    total = sum(item['price'] * item['quantity'] for item in cart_items)
    
    new_order = Order(
        telegram_user_id=user_id,
        customer_name=user_name,
        total_amount=total
    )
    db.session.add(new_order)
    db.session.commit()

    for item in cart_items:
        order_item = OrderItem(
            order_id=new_order.id,
            item_name=item['name'],
            price=item['price'],
            quantity=item['quantity']
        )
        db.session.add(order_item)

    db.session.commit()
    return jsonify({"success": True, "order_id": new_order.id})

# 4. Success Page
@main.route('/success/<int:order_id>')
def success(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('success.html', order=order)