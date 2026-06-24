from database.db import Database


class ProductDB:

    def __init__(self):

        self.db = Database()



    # ================= CREATE PRODUCT =================

    def add_product(
        self,
        name,
        category_id,
        supplier_id,
        buy_price,
        sell_price,
        quantity,
        serial_number,
        user_id
    ):

        query = """
        INSERT INTO products
        (
            name,
            category_id,
            supplier_id,
            buy_price,
            sell_price,
            quantity,
            serial_number,
            user_id
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """


        self.db.execute(
            query,
            (
                name,
                category_id,
                supplier_id,
                buy_price,
                sell_price,
                quantity,
                serial_number,
                user_id
            )
        )



    # ================= GET ALL PRODUCTS =================

    def get_products(self):

        query = """
        SELECT

            p.id,

            p.name,

            p.buy_price,

            p.sell_price,

            p.quantity,

            p.serial_number,

            p.created_at,


            c.name AS category_name,

            s.name AS supplier_name,

            u.full_name AS user_name


        FROM products p


        LEFT JOIN categories c

        ON p.category_id = c.id


        LEFT JOIN suppliers s

        ON p.supplier_id = s.id


        LEFT JOIN users u

        ON p.user_id = u.id


        ORDER BY p.id DESC
        """


        return self.db.fetch_all(query)



    # ================= GET ONE PRODUCT =================

    def get_product(self, product_id):

        query = """
        SELECT

            p.id,

            p.name,

            p.buy_price,

            p.sell_price,

            p.quantity,

            p.serial_number,

            p.created_at,


            c.name AS category_name,

            s.name AS supplier_name,

            u.full_name AS user_name


        FROM products p


        LEFT JOIN categories c

        ON p.category_id = c.id


        LEFT JOIN suppliers s

        ON p.supplier_id = s.id


        LEFT JOIN users u

        ON p.user_id = u.id


        WHERE p.id=?
        """


        return self.db.fetch_one(
            query,
            (product_id,)
        )



    # ================= UPDATE PRODUCT =================

    def update_product(
        self,
        product_id,
        name,
        category_id,
        supplier_id,
        buy_price,
        sell_price,
        quantity,
        serial_number
    ):


        query = """
        UPDATE products

        SET

            name=?,

            category_id=?,

            supplier_id=?,

            buy_price=?,

            sell_price=?,

            quantity=?,

            serial_number=?


        WHERE id=?
        """


        self.db.execute(
            query,
            (
                name,
                category_id,
                supplier_id,
                buy_price,
                sell_price,
                quantity,
                serial_number,
                product_id
            )
        )



    # ================= DELETE PRODUCT =================

    def delete_product(self, product_id):

        query = """
        DELETE FROM products

        WHERE id=?
        """


        self.db.execute(
            query,
            (product_id,)
        )



    # ================= TOTAL SALES =================

    def get_total_sales(self):

        query = """
        SELECT

            COALESCE(
                SUM(total_amount),
                0
            ) AS total_sales

        FROM sales
        """


        result = self.db.fetch_one(query)


        return result["total_sales"]



    # ================= TODAY SALES =================

    def get_today_sales(self):

        query = """
        SELECT

            COALESCE(
                SUM(total_amount),
                0
            ) AS today_sales

        FROM sales


        WHERE date(sale_date)=date('now')
        """


        result = self.db.fetch_one(query)


        return result["today_sales"]



    # ================= LOW STOCK =================

    def get_low_stock(self, limit=5):

        query = """
        SELECT

            id,

            name,

            quantity


        FROM products


        WHERE quantity <= 5


        ORDER BY quantity ASC


        LIMIT ?
        """


        return self.db.fetch_all(
            query,
            (limit,)
        )



    # ================= TOTAL PRODUCTS =================

    def get_total_products(self):

        query = """
        SELECT

            COUNT(*) AS total_products

        FROM products
        """


        result = self.db.fetch_one(query)


        return result["total_products"]
    

        # ================= SEARCH PRODUCTS =================

    def search_products(self, keyword):

        query = """
        SELECT

            p.id,

            p.name,

            p.sell_price,

            p.quantity,

            c.name AS category_name


        FROM products p


        LEFT JOIN categories c

        ON p.category_id = c.id


        WHERE p.name LIKE ?


        ORDER BY p.name ASC
        """


        return self.db.fetch_all(
            query,
            (f"%{keyword}%",)
        )
    

        # ================= CREATE SALE =================

    def create_sale(self, customer, total_amount, user_id):

        query = """
        INSERT INTO sales
        (
            customer,
            total_amount,
            user_id
        )

        VALUES (?, ?, ?)
        """

        self.db.execute(
            query,
            (
                customer,
                total_amount,
                user_id
            )
        )


        result = self.db.fetch_one(
            "SELECT last_insert_rowid() AS id"
        )


        return result["id"]



    # ================= ADD SALE ITEM =================

    def add_sale_item(
            self,
            sale_id,
            product_id,
            quantity,
            price
    ):

        query = """
        INSERT INTO sale_items
        (
            sale_id,
            product_id,
            quantity,
            price
        )

        VALUES (?, ?, ?, ?)
        """


        self.db.execute(
            query,
            (
                sale_id,
                product_id,
                quantity,
                price
            )
        )


        self.db.execute(
            """
            UPDATE products

            SET quantity = quantity - ?

            WHERE id=?
            """,
            (
                quantity,
                product_id
            )
        )



    def create_sale(
            self,
            customer,
            total_amount,
            user_id
        ):

            query = """
            INSERT INTO sales
            (
                customer,
                total_amount,
                user_id
            )

            VALUES (?, ?, ?)
            """


            self.db.execute(
                query,
                (
                    customer,
                    total_amount,
                    user_id
                )
            )


            result = self.db.fetch_one(
                """
                SELECT last_insert_rowid() AS id
                """
            )


            return result["id"]

