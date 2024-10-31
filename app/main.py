import os
from fastapi import FastAPI, Depends, HTTPException, Path, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from .database.models import User, Product, Order, OrderItem, Session as db_session
from .database.db_operations import *  # Import all db operations
from .schemas import *  # Import all schemas
from typing import List
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

app = FastAPI()
security = HTTPBasic()


def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    # Replace with your actual authentication logic
    correct_username = os.getenv("API_USERNAME")
    correct_password = os.getenv("API_PASSWORD")
    if credentials.username == correct_username and credentials.password == correct_password:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Basic"},
    )


# User endpoints
@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_api(user: UserCreate, db: Session = Depends(get_db), authenticated: bool = Depends(authenticate)):
    created_user = create_user(
        db, user.username, user.email, user.password_hash)
    return created_user


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user_api(user_id: int, db: Session = Depends(get_db), authenticated: bool = Depends(authenticate)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user_api(user_id: int, user_update: UserCreate, db: Session = Depends(get_db), authenticated: bool = Depends(authenticate)):
    updated_user = update_user(
        db, user_id, user_update.username, user_update.email)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_api(user_id: int, db: Session = Depends(get_db), authenticated: bool = Depends(authenticate)):
    deleted_user = delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return


# Product endpoints
@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product_api(product: ProductCreate, db: Session = Depends(get_db), authenticated: bool = Depends(authenticate)):
    created_product = create_product(
        db, product.name, product.description, product.price)
    return created_product


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product_api(product_id: int, db: Session = Depends(get_db), authenticated: bool = Depends(authenticate)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product_api(product_id: int, product_update: ProductCreate, db: Session = Depends(get_db), authenticated: bool = Depends(authenticate)):
    updated_product = update_product(
        db, product_id, product_update.name, product_update.description, product_update.price)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_api(product_id: int, db: Session = Depends(get_db), authenticated: bool = Depends(authenticate)):
    deleted_product = delete_product(db, product_id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return


# Order Endpoints
@app.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order_api(order: OrderCreate, db: Session = Depends(get_db), authenticated: bool = Depends(authenticate)):
    created_order = create_order(db, order.user_id, order.total_amount)
    return created_order


@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order_api(order_id: int, db: Session = Depends(get_db), authenticated: bool = Depends(authenticate)):
    order = get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.put("/orders/{order_id}", response_model=OrderResponse)
def update_order_api(order_id: int, order_update: OrderCreate, db: Session = Depends(get_db), authenticated: bool = Depends(authenticate)):
    updated_order = update_order(db, order_id, order_update.total_amount)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order


@app.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_api(order_id: int, db: Session = Depends(get_db), authenticated: bool = Depends(authenticate)):
    deleted_order = delete_order(db, order_id)
    if not deleted_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return


# Order Item Endpoints
@app.post("/orders/{order_id}/items", response_model=OrderItemResponse, status_code=status.HTTP_201_CREATED)
def create_order_item_api(item: OrderItemCreate, order_id: int = Path(...), db: Session = Depends(get_db), authenticated: bool = Depends(authenticate)):
    created_item = create_order_item(
        db, order_id, item.product_id, item.quantity)
    return created_item


@app.get("/orders/{order_id}/items/{item_id}", response_model=OrderItemResponse)
def get_order_item_api(order_id: int, item_id: int, db: Session = Depends(get_db), authenticated: bool = Depends(authenticate)):
    order_item = get_order_item(db, item_id)
    if not order_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    if order_item.order_id != order_id:
        raise HTTPException(
            status_code=404, detail="Order item not found for this order")
    return order_item


@app.put("/orders/{order_id}/items/{item_id}", response_model=OrderItemResponse)
def update_order_item_api(order_id: int, item_id: int, item_update: OrderItemCreate, db: Session = Depends(get_db), authenticated: bool = Depends(authenticate)):
    updated_order_item = update_order_item(db, item_id, item_update.quantity)
    if not updated_order_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    if updated_order_item.order_id != order_id:
        raise HTTPException(
            status_code=404, detail="Order item not found for this order")
    return updated_order_item


@app.delete("/orders/{order_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_item_api(order_id: int, item_id: int, db: Session = Depends(get_db), authenticated: bool = Depends(authenticate)):
    deleted_order_item = delete_order_item(db, item_id)
    if not deleted_order_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    if deleted_order_item.order_id != order_id:
        raise HTTPException(
            status_code=404, detail="Order item not found for this order")
    return


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
