-- Clear old data
DELETE FROM order_items;
DELETE FROM orders;
DELETE FROM reservations;
DELETE FROM menu_items;
DELETE FROM menu_categories;
DELETE FROM dining_tables;
DELETE FROM customers;

-- Customers
INSERT INTO customers (name, email, phone) VALUES
('Alice Johnson', 'alice@example.com', '9876543210');

-- Dining Tables
INSERT INTO dining_tables (label, seats, active) VALUES
('T1', 2, 1),
('T2', 4, 1),
('T3', 6, 1),
('T4', 4, 0);

-- Menu Categories
INSERT INTO menu_categories (name, sort_order) VALUES
('Starters', 1),
('Main Course', 2),
('Desserts', 3),
('Drinks', 4);

-- Menu Items
INSERT INTO menu_items
(category_id, name, description, price_cents, available)
VALUES
(1, 'Garlic Bread', 'Toasted garlic bread', 199, 1),
(1, 'Tomato Soup', 'Creamy tomato soup', 249, 1),

(2, 'Veg Burger', 'Loaded veg burger', 349, 1),
(2, 'Chicken Pizza', '12 inch pizza', 699, 1),
(2, 'Pasta Alfredo', 'Creamy white sauce pasta', 499, 0),

(3, 'Brownie', 'Chocolate brownie', 299, 1),

(4, 'Coke', '300ml soft drink', 99, 1),
(4, 'Lemon Juice', 'Fresh lemonade', 149, 1);