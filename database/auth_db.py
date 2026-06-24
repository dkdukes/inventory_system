from database.db import Database


class AuthDB:

    def __init__(self):
        self.db = Database()

    # ---------------- LOGIN ----------------

    def login_user(self, email, password):

        query = """
        SELECT id, full_name, role
        FROM users
        WHERE email=? AND password=?
        """

        return self.db.fetch_one(query, (email, password))

    # ---------------- REGISTER ----------------

    def add_user(self, full_name, phone_number, email, password, role):

        query = """
        INSERT INTO users (full_name, phone_number, email, password, role)
        VALUES (?, ?, ?, ?, ?)
        """

        self.db.execute(query, (
            full_name,
            phone_number,
            email,
            password,
            role
        ))