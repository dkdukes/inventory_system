import sqlite3


class Database:

    def __init__(self):

        self.conn = sqlite3.connect("inventory.db")
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()

        self.create_tables()



    def create_tables(self):

        # USERS TABLE
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT,
                phone_number TEXT,
                email TEXT UNIQUE,
                password TEXT,
                role TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)


        # PRODUCTS TABLE
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                supplier TEXT,
                buy_price REAL,
                sell_price REAL,
                quantity INTEGER,
                serial_number TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        self.conn.commit()



    # ---------------- PRODUCTS ----------------

    def add_product(
        self,
        name,
        category,
        supplier,
        buy_price,
        sell_price,
        quantity,
        serial_number,
        user_id
    ):

        self.cursor.execute("""
            INSERT INTO products
            (name, category, supplier, buy_price, sell_price, quantity, serial_number, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            category,
            supplier,
            buy_price,
            sell_price,
            quantity,
            serial_number,
            user_id
        ))

        self.conn.commit()

    def add_user(self, full_name, phone_number, email, password, role):

        self.cursor.execute("""
            INSERT INTO users (full_name, phone_number, email, password, role)
            VALUES (?, ?, ?, ?, ?)
        """, (
            full_name,
            phone_number,
            email,
            password,
            role
        ))

        self.conn.commit()

    def get_products(self):

        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()

    def login_user(self, email, password):

        self.cursor.execute("""
            SELECT id, full_name, role
            FROM users
            WHERE email=? AND password=?
        """, (email, password))

        return self.cursor.fetchone()

    def delete_product(self, product_id):

        self.cursor.execute("""
            DELETE FROM products WHERE id=?
        """, (product_id,))

        self.conn.commit()