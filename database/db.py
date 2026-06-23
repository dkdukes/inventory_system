import sqlite3


class Database:

    def __init__(self):

        self.conn = sqlite3.connect("inventory.db")
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()

        self.create_tables()



    
    def execute(self, query, params=()):

        self.cursor.execute(
            query,
            params
        )

        self.conn.commit()



    def fetch_all(self, query, params=()):

        self.cursor.execute(
            query,
            params
        )

        return self.cursor.fetchall()



    def fetch_one(self, query, params=()):

        self.cursor.execute(
            query,
            params
        )

        return self.cursor.fetchone()



    def create_tables(self):

        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT,
                phone_number TEXT,
                email TEXT UNIQUE,
                password TEXT,
                role TEXT
            );


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

                FOREIGN KEY(user_id)
                REFERENCES users(id)
            );



            CREATE TABLE IF NOT EXISTS sales (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                customer TEXT,

                total_amount REAL,

                sale_date TEXT DEFAULT CURRENT_TIMESTAMP,

                user_id INTEGER,

                FOREIGN KEY(user_id)
                REFERENCES users(id)
            );



            CREATE TABLE IF NOT EXISTS sale_items (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                sale_id INTEGER,

                product_id INTEGER,

                quantity INTEGER,

                price REAL,


                FOREIGN KEY(sale_id)
                REFERENCES sales(id),


                FOREIGN KEY(product_id)
                REFERENCES products(id)

            );
                                  
            CREATE TABLE IF NOT EXISTS categories(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL UNIQUE,

                description TEXT,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            );
                                  

            CREATE TABLE IF NOT EXISTS suppliers(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL,

                phone TEXT,

                email TEXT,

                address TEXT,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            );

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

    


 # ---------------- SALES ----------------



    def create_sale(
            self,
            customer,
            total_amount,
            user_id
    ):

        self.cursor.execute("""
            INSERT INTO sales
            (customer,total_amount,user_id)

            VALUES (?,?,?)

        """,
        (
            customer,
            total_amount,
            user_id
        ))


        self.conn.commit()


        return self.cursor.lastrowid
    


    def add_sale_item(
            self,
            sale_id,
            product_id,
            quantity,
            price
    ):

        self.cursor.execute("""
            INSERT INTO sale_items
            (
                sale_id,
                product_id,
                quantity,
                price
            )

            VALUES (?,?,?,?)

        """,
        (
            sale_id,
            product_id,
            quantity,
            price
        ))


        self.cursor.execute("""
            UPDATE products

            SET quantity = quantity - ?

            WHERE id=?

        """,
        (
            quantity,
            product_id
        ))


        self.conn.commit()
    


    # ENABLE SEARCH OF PRODUCTS

    def search_products(self, keyword):

        self.cursor.execute("""
            SELECT id, name, sell_price, quantity
            FROM products
            WHERE name LIKE ?
        """, (
            f"%{keyword}%",
        ))

        return self.cursor.fetchall()
    


    def get_total_sales(self):

        self.cursor.execute("""
            SELECT SUM(total_amount) FROM sales
        """)

        result = self.cursor.fetchone()[0]

        return result or 0
    

    def get_today_sales(self):

        self.cursor.execute("""
            SELECT SUM(total_amount)
            FROM sales
            WHERE date(sale_date) = date('now')
        """)

        result = self.cursor.fetchone()[0]

        return result or 0
    

    def get_total_products(self):

        self.cursor.execute("""
            SELECT COUNT(*) FROM products
        """)

        return self.cursor.fetchone()[0]
    

    def get_low_stock(self, limit=5):

        self.cursor.execute("""
            SELECT name, quantity
            FROM products
            WHERE quantity <= 5
            ORDER BY quantity ASC
            LIMIT ?
        """, (limit,))

        return self.cursor.fetchall()
    
    def get_total_customers(self):

        self.cursor.execute("""
            SELECT COUNT(DISTINCT customer)
            FROM sales
        """)

        return self.cursor.fetchone()[0]