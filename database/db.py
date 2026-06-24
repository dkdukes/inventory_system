import sqlite3


import sqlite3


class Database:

    _instance = None


    def __new__(cls):

        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)

        return cls._instance



    def __init__(self):

        # prevent reconnecting every time Database() is called
        if hasattr(self, "conn"):
            return


        self.conn = sqlite3.connect(
            "inventory.db",
            timeout=10
        )


        # return rows as dictionaries
        self.conn.row_factory = sqlite3.Row


        # enable foreign keys
        self.conn.execute(
            "PRAGMA foreign_keys = ON"
        )


        # improve concurrent access
        self.conn.execute(
            "PRAGMA journal_mode=WAL"
        )


        self.cursor = self.conn.cursor()


        self.create_tables()



    # ================= EXECUTE =================

    def execute(self, query, params=()):

        try:

            self.cursor.execute(
                query,
                params
            )

            self.conn.commit()


        except sqlite3.Error as e:

            self.conn.rollback()
            raise e



    # ================= FETCH ALL =================

    def fetch_all(self, query, params=()):

        self.cursor.execute(
            query,
            params
        )

        rows = self.cursor.fetchall()


        return [
            dict(row)
            for row in rows
        ]



    # ================= FETCH ONE =================

    def fetch_one(self, query, params=()):

        self.cursor.execute(
            query,
            params
        )

        row = self.cursor.fetchone()


        return dict(row) if row else None



    # ================= CLOSE =================

    def close(self):

        if self.conn:

            self.conn.close()

            self.conn = None



    # ================= TABLES =================

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


        CREATE TABLE IF NOT EXISTS categories (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL UNIQUE,

            description TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        );


        CREATE TABLE IF NOT EXISTS suppliers (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            phone TEXT,

            email TEXT,

            address TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        );



        CREATE TABLE IF NOT EXISTS products (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            buy_price REAL DEFAULT 0,

            sell_price REAL DEFAULT 0,

            quantity INTEGER DEFAULT 0 
            CHECK(quantity >= 0),

            serial_number TEXT UNIQUE,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP,

            user_id INTEGER,

            category_id INTEGER,

            supplier_id INTEGER,


            FOREIGN KEY(user_id)
            REFERENCES users(id),


            FOREIGN KEY(category_id)
            REFERENCES categories(id),


            FOREIGN KEY(supplier_id)
            REFERENCES suppliers(id)

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


        """)


        self.conn.commit()