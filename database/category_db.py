from database.db import Database



class CategoryDB:


    def __init__(self):

        self.db = Database()



    def add_category(self,name,description):

        query = """
        INSERT INTO categories(name,description)
        VALUES(?,?)
        """

        self.db.execute(
            query,
            (name,description)
        )



    def get_categories(self):

        query = """
        SELECT * FROM categories
        """

        return self.db.fetch_all(query)



    def delete_category(self,id):

        query="""

        DELETE FROM categories
        WHERE id=?

        """

        self.db.execute(
            query,
            (id,)
        )



    def update_category(self,id,name,description):

        query="""

        UPDATE categories

        SET name=?,
            description=?

        WHERE id=?

        """

        self.db.execute(
            query,
            (
                name,
                description,
                id
            )
        )