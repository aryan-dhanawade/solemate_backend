from flask import Flask
from utils.db import configure_app, db
from routes.auth_routes import auth_bp
from routes.category_routes import category_bp
from routes.product_routes import product_bp
from routes.order_routes import order_bp
from routes.contact_routes import contact_bp
from routes.payment_routes import payment_bp
from flask_cors import CORS

app = Flask(__name__)
configure_app(app)
CORS(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(category_bp, url_prefix='/api')
app.register_blueprint(product_bp, url_prefix='/api')
app.register_blueprint(order_bp, url_prefix='/api')
app.register_blueprint(payment_bp, url_prefix='/api')
app.register_blueprint(contact_bp, url_prefix='/api')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(host="0.0.0.0", port=5000)
