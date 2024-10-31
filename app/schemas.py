﻿from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    created_at: datetime


class UserCreate(BaseModel):  # Schema for creating a new user (excluding user_id)
    username: str
    email: str
    password_hash: str


class ProductResponse(BaseModel):
    product_id: int
    name: str
    description: str | None = None  # Optional description
    price: Decimal
    created_at: datetime


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: Decimal


class OrderItemResponse(BaseModel):
    orderitem_id: int
    order_id: int
    product_id: int
    quantity: int


class OrderItemCreate(BaseModel):  # For creating OrderItems
    product_id: int
    quantity: int


class OrderResponse(BaseModel):
    order_id: int
    user_id: int
    order_date: datetime
    total_amount: Decimal


class OrderCreate(BaseModel):  # Don't include order_id in the request
    user_id: int
    total_amount: Decimal