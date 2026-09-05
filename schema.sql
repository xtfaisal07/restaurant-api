PRAGMA foreign_keys = ON;

-- =========================
-- CUSTOMERS
-- =========================
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT
);

-- =========================
-- DINING TABLES
-- =========================
CREATE TABLE dining_tables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT NOT NULL UNIQUE,
    seats INTEGER NOT NULL,
    active INTEGER NOT NULL DEFAULT 1
);

-- =========================
-- RESERVATIONS
-- =========================
CREATE TABLE reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    dining_table_id INTEGER NOT NULL,
    reservation_time TEXT NOT NULL,
    party_size INTEGER NOT NULL,
    status TEXT NOT NULL,

    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (dining_table_id) REFERENCES dining_tables(id)
);

-- =========================
-- MENU CATEGORIES
-- =========================
CREATE TABLE menu_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    sort_order INTEGER NOT NULL
);

-- =========================
-- MENU ITEMS
-- =========================
CREATE TABLE menu_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    price_cents INTEGER NOT NULL,
    available INTEGER NOT NULL DEFAULT 1,

    FOREIGN KEY (category_id) REFERENCES menu_categories(id)
);

-- =========================
-- ORDERS
-- =========================
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    dining_table_id INTEGER,
    reservation_id INTEGER,
    status TEXT NOT NULL,
    total_cents INTEGER NOT NULL,
    created_at TEXT NOT NULL,

    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (dining_table_id) REFERENCES dining_tables(id),
    FOREIGN KEY (reservation_id) REFERENCES reservations(id)
);

-- =========================
-- ORDER ITEMS
-- =========================
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    menu_item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price_cents INTEGER NOT NULL,
    line_total_cents INTEGER NOT NULL,

    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
);

-- =========================
-- INDEXES
-- =========================
CREATE INDEX idx_reservation_time
ON reservations(reservation_time);

CREATE INDEX idx_orders_customer
ON orders(customer_id);

CREATE INDEX idx_order_items_order
ON order_items(order_id);