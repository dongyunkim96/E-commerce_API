from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

# Initialize Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Dongyun123*@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT configuration
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Replace with a strong, unique key
jwt = JWTManager(app)

# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Define database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class OrderProduct(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)

# Define Marshmallow schemas
class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
    id = ma.auto_field()
    name = ma.auto_field()
    address = ma.auto_field()
    email = ma.auto_field()

class OrderSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Order
        include_fk = True
    id = ma.auto_field()
    order_date = ma.auto_field()
    user_id = ma.auto_field()

class ProductSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Product
    id = ma.auto_field()
    product_name = ma.auto_field()
    price = ma.auto_field()

# Create schema instances
user_schema = UserSchema()
users_schema = UserSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# User registration endpoint
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(
        name=data['name'],
        address=data['address'],
        email=data['email'],
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(user_schema.dump(new_user)), 201

# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))
        return jsonify({'access_token': token}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

# User endpoints
@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    users = User.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'users': users_schema.dump(users.items),
        'total': users.total,
        'pages': users.pages,
        'current_page': users.page
    })

@app.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user_schema.dump(user))

@app.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.json
    user.name = data['name']
    user.address = data['address']
    user.email = data['email']
    db.session.commit()
    return jsonify(user_schema.dump(user))

@app.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return '', 204

# Product endpoints
@app.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    products = Product.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'products': products_schema.dump(products.items),
        'total': products.total,
        'pages': products.pages,
        'current_page': products.page
    })

@app.route('/products/<int:id>', methods=['GET'])
@jwt_required()
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product_schema.dump(product))

@app.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    data = request.json
    new_product = Product(product_name=data['product_name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify(product_schema.dump(new_product)), 201

@app.route('/products/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.json
    product.product_name = data['product_name']
    product.price = data['price']
    db.session.commit()
    return jsonify(product_schema.dump(product))

@app.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return '', 204

# Order endpoints
@app.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    data = request.json
    new_order = Order(user_id=data['user_id'], order_date=data.get('order_date', datetime.utcnow()))
    db.session.add(new_order)
    db.session.commit()
    return jsonify(order_schema.dump(new_order)), 201

@app.route('/orders/<int:order_id>/add_product/<int:product_id>', methods=['PUT'])
@jwt_required()
def add_product_to_order(order_id, product_id):
    order_product = OrderProduct(order_id=order_id, product_id=product_id)
    db.session.add(order_product)
    db.session.commit()
    return '', 204

@app.route('/orders/<int:order_id>/remove_product/<int:product_id>', methods=['DELETE'])
@jwt_required()
def remove_product_from_order(order_id, product_id):
    order_product = OrderProduct.query.filter_by(order_id=order_id, product_id=product_id).first_or_404()
    db.session.delete(order_product)
    db.session.commit()
    return '', 204

@app.route('/orders/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_orders_by_user(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify(orders_schema.dump(orders))

@app.route('/orders/<int:order_id>/products', methods=['GET'])
@jwt_required()
def get_products_in_order(order_id):
    products = db.session.query(Product).join(OrderProduct).filter(OrderProduct.order_id == order_id).all()
    return jsonify(products_schema.dump(products))

@app.route('/orders/<int:order_id>/total', methods=['GET'])
@jwt_required()
def calculate_order_total(order_id):
    products = db.session.query(Product).join(OrderProduct).filter(OrderProduct.order_id == order_id).all()
    total = sum(product.price for product in products)
    return jsonify({'order_id': order_id, 'total_cost': total})

@app.route('/orders/user/<int:user_id>/latest', methods=['GET'])
@jwt_required()
def get_latest_order(user_id):
    order = Order.query.filter_by(user_id=user_id).order_by(Order.order_date.desc()).first()
    if order:
        return jsonify(order_schema.dump(order))
    return jsonify({'error': 'No orders found for this user'}), 404

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
