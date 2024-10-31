#!/bin/bash

export PGPASSWORD="$POSTGRES_PASSWORD"

psql -U postgres -c "CREATE DATABASE ecommerce;"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "ecommerce" <<-EOSQL
    CREATE TABLE Users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE Products (
        product_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE Orders (
        order_id SERIAL PRIMARY KEY,
        user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total_amount DECIMAL(10, 2) NOT NULL CHECK (total_amount >= 0)
    );

    CREATE TABLE Order_Items (
        orderitem_id SERIAL PRIMARY KEY,
        order_id INT REFERENCES Orders(order_id) ON DELETE CASCADE,
        product_id INT REFERENCES Products(product_id) ON DELETE CASCADE,
        quantity INT NOT NULL CHECK (quantity > 0)
    );
EOSQL