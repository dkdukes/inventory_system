from database.db import Database


class SupplierDB:


    def __init__(self):

        self.db = Database()



    def add_supplier(
            self,
            name,
            phone,
            email,
            address
        ):


        query = """

        INSERT INTO suppliers
        (
            name,
            phone,
            email,
            address
        )

        VALUES(?,?,?,?)

        """


        self.db.execute(
            query,
            (
                name,
                phone,
                email,
                address
            )
        )




    def get_suppliers(self):

        query = """

        SELECT *
        FROM suppliers

        """


        return self.db.fetch_all(query)




    def delete_supplier(self,id):

        query = """

        DELETE FROM suppliers
        WHERE id=?

        """


        self.db.execute(
            query,
            (id,)
        )




    def update_supplier(
            self,
            id,
            name,
            phone,
            email,
            address
        ):


        query = """

        UPDATE suppliers

        SET
        name=?,
        phone=?,
        email=?,
        address=?

        WHERE id=?

        """


        self.db.execute(
            query,
            (
                name,
                phone,
                email,
                address,
                id
            )
        )