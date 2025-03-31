from flask import Flask
from utils.db import configure_app, db
from flask_migrate import Migrate
from routes.auth_routes import auth_bp
from routes.category_routes import category_bp
from routes.product_routes import product_bp
from routes.order_routes import order_bp
from routes.payment_routes import payment_bp
from routes.contact_routes import contact_bp
from flask_cors import CORS


app = Flask(__name__)
configure_app(app)
migrate = Migrate(app, db)
CORS(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(category_bp, url_prefix='/api')
app.register_blueprint(product_bp, url_prefix='/api')
app.register_blueprint(order_bp, url_prefix='/api')
app.register_blueprint(payment_bp, url_prefix='/api')
app.register_blueprint(contact_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
