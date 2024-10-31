from sqlalchemy.orm import Session
from app.database.models import User, Product, Order, OrderItem


def create_user(db: Session, username: str, email: str, password_hash: str):
    new_user = User(username=username, email=email,
                    password_hash=password_hash)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()


def update_user(db: Session, user_id: int, username: str = None, email: str = None):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        if username:
            user.username = username
        if email:
            user.email = email
        db.commit()
        db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user


# Product CRUD Operations
def create_product(db: Session, name: str, description: str, price: float):
    new_product = Product(name=name, description=description, price=price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.product_id == product_id).first()


def update_product(db: Session, product_id: int, name: str = None, description: str = None, price: float = None):
    product = db.query(Product).filter(
        Product.product_id == product_id).first()
    if product:
        if name:
            product.name = name
        if description:
            product.description = description
        if price:
            product.price = price
        db.commit()
        db.refresh(product)
    return product


def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(
        Product.product_id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return product


# Order CRUD Operations
def create_order(db: Session, user_id: int, total_amount: float):
    new_order = Order(user_id=user_id, total_amount=total_amount)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.order_id == order_id).first()


def update_order(db: Session, order_id: int, total_amount: float = None):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if order:
        if total_amount:
            order.total_amount = total_amount
        db.commit()
        db.refresh(order)
    return order


def delete_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if order:
        db.delete(order)
        db.commit()
    return order


# OrderItem CRUD Operations
def create_order_item(db: Session, order_id: int, product_id: int, quantity: int):
    new_order_item = OrderItem(
        order_id=order_id, product_id=product_id, quantity=quantity)
    db.add(new_order_item)
    db.commit()
    db.refresh(new_order_item)
    return new_order_item


def get_order_item(db: Session, orderitemid: int):
    return db.query(OrderItem).filter(OrderItem.orderitemid == orderitemid).first()


def update_order_item(db: Session, orderitemid: int, quantity: int = None):
    order_item = db.query(OrderItem).filter(
        OrderItem.orderitemid == orderitemid).first()
    if order_item:
        if quantity:
            order_item.quantity = quantity
        db.commit()
        db.refresh(order_item)
    return order_item


def delete_order_item(db: Session, orderitemid: int):
    order_item = db.query(OrderItem).filter(
        OrderItem.orderitemid == orderitemid).first()
    if order_item:
        db.delete(order_item)
        db.commit()
    return order_item
