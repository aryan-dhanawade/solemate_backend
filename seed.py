import random
import datetime
from faker import Faker

fake = Faker()

from utils.db import db
from models.category import Category
from models.product import Product
from models.customer import Customer
from models.order import Order
from models.order_items import OrderItem
from models.payment import Payment
from utils.auth import hash_password
from app import app  # or import your Flask app from manage.py if that's where it's defined

with app.app_context():
    # Optional: Drop all tables (caution in production)
    # db.drop_all()
    # db.create_all()

    # Seed Categories
    category_names = ["Sneakers", "Formal Shoes", "Athletic Shoes", "Boots", "Sandals"]
    categories = []
    for name in category_names:
        cat = Category(name=name)
        db.session.add(cat)
        categories.append(cat)
    db.session.commit()

    # Seed Products (20 products)
    products = []
    for i in range(20):
        category = random.choice(categories)
        product = Product(
            name=f"{fake.word().capitalize()} {fake.word().capitalize()}",
            description=fake.sentence(),
            price=round(random.uniform(50, 200), 2),
            stock_quantity=random.randint(10, 100),
            category_id=category.category_id
        )
        db.session.add(product)
        products.append(product)
    db.session.commit()

    # Seed Customers (10 customers)
    customers = []
    for i in range(10):
        customer = Customer(
            name=fake.name(),
            email=fake.unique.email(),
            phone=fake.phone_number()[:20],
            address=fake.address(),
            password=hash_password("password123")
        )
        db.session.add(customer)
        customers.append(customer)
    db.session.commit()

    # Seed Orders and Order Items for each Customer
    orders = []
    for customer in customers:
        num_orders = random.randint(1, 3)
        for _ in range(num_orders):
            order_date = fake.date_between(start_date='-1y', end_date='today')
            # Randomly select between 1 to 4 products for this order
            order_products = random.sample(products, random.randint(1, 4))
            total_amount = 0
            order = Order(
                order_date=order_date,
                total_amount=0,  # we'll update this after calculating order items
                status=random.choice(["Pending", "Shipped", "Delivered"]),
                customer_id=customer.customer_id
            )
            db.session.add(order)
            db.session.commit()  # Commit to generate order_id

            # Add order items and update total_amount
            for product in order_products:
                quantity = random.randint(1, 5)
                item_total = product.price * quantity
                total_amount += item_total

                order_item = OrderItem(
                    quantity=quantity,
                    price=product.price,
                    order_id=order.order_id,
                    product_id=product.product_id
                )
                db.session.add(order_item)
                # Update product stock (ensure it doesn't go negative)
                product.stock_quantity = max(product.stock_quantity - quantity, 0)
            # Update the order's total amount
            order.total_amount = total_amount
            db.session.commit()
            orders.append(order)

    # Seed Payments for orders with status "Shipped" or "Delivered"
    for order in orders:
        if order.status in ["Shipped", "Delivered"]:
            payment = Payment(
                amount=order.total_amount,
                payment_date=order.order_date + datetime.timedelta(days=random.randint(0, 5)),
                payment_method=random.choice(["Credit Card", "PayPal", "Debit Card"]),
                order_id=order.order_id
            )
            db.session.add(payment)
    db.session.commit()

    print("Database seeded with extensive sample data!")
