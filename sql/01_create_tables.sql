-- E-Commerce Sales & Customer Analytics
-- Database and table structure

CREATE DATABASE IF NOT EXISTS ecommerce_analytics;

USE ecommerce_analytics;


-- 1. Customers
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    age INT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    signup_date DATE NOT NULL
);


-- 2. Products
CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(100) NOT NULL,
    brand VARCHAR(100) NOT NULL,
    cost_price DECIMAL(12,2) NOT NULL,
    selling_price DECIMAL(12,2) NOT NULL
);


-- 3. Orders
CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    discount DECIMAL(5,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);


-- 4. Order Items
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);