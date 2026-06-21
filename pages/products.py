import customtkinter as ctk
from database.db import Database


class Products(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.db = Database()

        self.create_ui()
        self.load_products()



    # ---------------- UI ----------------

    def create_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Products Module",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=10)



        # FORM
        form = ctk.CTkFrame(self)
        form.pack(pady=10, fill="x")



        self.name = ctk.CTkEntry(form, placeholder_text="Product Name")
        self.name.grid(row=0, column=0, padx=5)

        self.category = ctk.CTkEntry(form, placeholder_text="Category")
        self.category.grid(row=0, column=1, padx=5)

        self.supplier = ctk.CTkEntry(form, placeholder_text="Supplier")
        self.supplier.grid(row=0, column=2, padx=5)

        self.buy_price = ctk.CTkEntry(form, placeholder_text="Buy Price")
        self.buy_price.grid(row=0, column=3, padx=5)

        self.sell_price = ctk.CTkEntry(form, placeholder_text="Sell Price")
        self.sell_price.grid(row=0, column=4, padx=5)

        self.qty = ctk.CTkEntry(form, placeholder_text="Quantity")
        self.qty.grid(row=0, column=5, padx=5)

        self.serial = ctk.CTkEntry(form, placeholder_text="Serial No")
        self.serial.grid(row=0, column=6, padx=5)



        add_btn = ctk.CTkButton(
            form,
            text="Add Product",
            command=self.add_product
        )
        add_btn.grid(row=0, column=7, padx=10)



        # SEARCH
        self.search = ctk.CTkEntry(self, placeholder_text="Search product...")
        self.search.pack(fill="x", padx=20, pady=10)
        self.search.bind("<KeyRelease>", self.search_product)



        # TABLE
        self.table_frame = ctk.CTkScrollableFrame(self)
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=10)



    # ---------------- ADD PRODUCT ----------------

    def add_product(self):

        name = self.name.get()
        category = self.category.get()
        supplier = self.supplier.get()

        buy_price = float(self.buy_price.get() or 0)
        sell_price = float(self.sell_price.get() or 0)

        qty = int(self.qty.get() or 0)
        serial = self.serial.get()

        from auth.session import Session

        user_id = Session.current_user["id"]


        self.db.add_product(
            name,
            category,
            supplier,
            buy_price,
            sell_price,
            qty,
            serial,
            user_id
        )

        self.clear_fields()
        self.load_products()



    # ---------------- LOAD PRODUCTS ----------------

    def load_products(self):

        for widget in self.table_frame.winfo_children():
            widget.destroy()


        products = self.db.get_products()


        for p in products:

            row = ctk.CTkFrame(self.table_frame)
            row.pack(fill="x", pady=2)



            ctk.CTkLabel(row, text=p[1], width=120).pack(side="left")
            ctk.CTkLabel(row, text=p[2], width=100).pack(side="left")
            ctk.CTkLabel(row, text=p[3], width=100).pack(side="left")
            ctk.CTkLabel(row, text=p[4], width=80).pack(side="left")
            ctk.CTkLabel(row, text=p[5], width=80).pack(side="left")
            ctk.CTkLabel(row, text=p[6], width=60).pack(side="left")
            ctk.CTkLabel(row, text=p[7], width=100).pack(side="left")
            ctk.CTkLabel(row, text=p[8], width=160).pack(side="left")  # created_at



            delete_btn = ctk.CTkButton(
                row,
                text="Delete",
                width=80,
                fg_color="red",
                command=lambda id=p[0]: self.delete_product(id)
            )

            delete_btn.pack(side="right", padx=10)



    # ---------------- DELETE ----------------

    def delete_product(self, product_id):

        self.db.delete_product(product_id)
        self.load_products()



    # ---------------- SEARCH ----------------

    def search_product(self, event):

        query = self.search.get().lower()


        for widget in self.table_frame.winfo_children():
            widget.destroy()


        products = self.db.get_products()


        for p in products:

            if query in p[1].lower():

                row = ctk.CTkFrame(self.table_frame)
                row.pack(fill="x", pady=2)



                ctk.CTkLabel(row, text=p[1], width=120).pack(side="left")
                ctk.CTkLabel(row, text=p[2], width=100).pack(side="left")
                ctk.CTkLabel(row, text=p[3], width=100).pack(side="left")
                ctk.CTkLabel(row, text=p[4], width=80).pack(side="left")
                ctk.CTkLabel(row, text=p[5], width=80).pack(side="left")
                ctk.CTkLabel(row, text=p[6], width=60).pack(side="left")
                ctk.CTkLabel(row, text=p[7], width=100).pack(side="left")
                ctk.CTkLabel(row, text=p[8], width=160).pack(side="left")



    # ---------------- CLEAR FIELDS ----------------

    def clear_fields(self):

        self.name.delete(0, "end")
        self.category.delete(0, "end")
        self.supplier.delete(0, "end")
        self.buy_price.delete(0, "end")
        self.sell_price.delete(0, "end")
        self.qty.delete(0, "end")
        self.serial.delete(0, "end")