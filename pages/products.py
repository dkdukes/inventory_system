import customtkinter as ctk

from database.product_db import ProductDB
from database.category_db import CategoryDB
from database.supplier_db import SupplierDB
from auth.session import Session


class Products(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.db = ProductDB()
        self.category_db = CategoryDB()
        self.supplier_db = SupplierDB()

        self.category_map = {}
        self.supplier_map = {}

        self.create_widgets()
        self.load_dropdowns()
        self.load_products()


    # ================= UI =================

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="Product Management",
            font=("Arial", 28, "bold")
        )

        title.pack(pady=15)


        # ================= FORM =================

        form = ctk.CTkFrame(self)
        form.pack(fill="x", padx=20, pady=10)


        self.name = ctk.CTkEntry(
            form,
            placeholder_text="Product Name"
        )
        self.name.pack(pady=5, fill="x")


        self.buy_price = ctk.CTkEntry(
            form,
            placeholder_text="Buy Price"
        )
        self.buy_price.pack(pady=5, fill="x")


        self.sell_price = ctk.CTkEntry(
            form,
            placeholder_text="Sell Price"
        )
        self.sell_price.pack(pady=5, fill="x")


        self.quantity = ctk.CTkEntry(
            form,
            placeholder_text="Quantity"
        )
        self.quantity.pack(pady=5, fill="x")


        self.serial = ctk.CTkEntry(
            form,
            placeholder_text="Serial Number"
        )
        self.serial.pack(pady=5, fill="x")


        # CATEGORY

        self.category_var = ctk.StringVar()

        self.category_menu = ctk.CTkOptionMenu(
            form,
            variable=self.category_var
        )

        self.category_menu.pack(
            pady=5,
            fill="x"
        )


        # SUPPLIER

        self.supplier_var = ctk.StringVar()

        self.supplier_menu = ctk.CTkOptionMenu(
            form,
            variable=self.supplier_var
        )

        self.supplier_menu.pack(
            pady=5,
            fill="x"
        )


        add_btn = ctk.CTkButton(
            form,
            text="Add Product",
            command=self.add_product
        )

        add_btn.pack(pady=10)



        # ================= TABLE HEADER =================

        header = ctk.CTkFrame(self)

        header.pack(
            fill="x",
            padx=20
        )


        columns = [
            "ID",
            "Name",
            "Buy",
            "Sell",
            "Qty",
            "Category",
            "Supplier",
            "User"
        ]


        for col in columns:

            label = ctk.CTkLabel(
                header,
                text=col,
                font=("Arial", 12, "bold")
            )

            label.pack(
                side="left",
                expand=True
            )


        # ================= TABLE =================

        self.table_frame = ctk.CTkScrollableFrame(self)

        self.table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )



    # ================= DROPDOWNS =================


    def load_dropdowns(self):

        categories = self.category_db.get_categories()

        suppliers = self.supplier_db.get_suppliers()


        self.category_map = {

            category["name"]: category["id"]

            for category in categories

        }


        self.supplier_map = {

            supplier["name"]: supplier["id"]

            for supplier in suppliers

        }


        self.category_menu.configure(
            values=list(self.category_map.keys())
        )


        self.supplier_menu.configure(
            values=list(self.supplier_map.keys())
        )



    # ================= ADD PRODUCT =================


    def add_product(self):

        if not Session.current_user:
            return


        self.db.add_product(

            self.name.get(),

            self.category_map[
                self.category_var.get()
            ],

            self.supplier_map[
                self.supplier_var.get()
            ],

            float(
                self.buy_price.get()
            ),

            float(
                self.sell_price.get()
            ),

            int(
                self.quantity.get()
            ),

            self.serial.get(),

            Session.current_user["id"]

        )


        self.clear_form()

        self.load_products()



    # ================= LOAD PRODUCTS =================


    def load_products(self):


        for widget in self.table_frame.winfo_children():

            widget.destroy()



        products = self.db.get_products()



        for product in products:


            row = ctk.CTkFrame(
                self.table_frame
            )

            row.pack(
                fill="x",
                pady=2
            )


            values = [

                product["id"],

                product["name"],

                product["buy_price"],

                product["sell_price"],

                product["quantity"],

                product["category_name"],

                product["supplier_name"],

                product["user_name"]

            ]


            for value in values:

                label = ctk.CTkLabel(
                    row,
                    text=str(value)
                )

                label.pack(
                    side="left",
                    expand=True
                )


            delete_btn = ctk.CTkButton(

                row,

                text="❌",

                width=40,

                fg_color="red",

                command=lambda pid=product["id"]:
                    self.delete_product(pid)

            )

            delete_btn.pack(
                side="right",
                padx=5
            )



    # ================= DELETE =================


    def delete_product(self, product_id):

        self.db.delete_product(product_id)

        self.load_products()



    # ================= CLEAR =================


    def clear_form(self):

        self.name.delete(0, "end")

        self.buy_price.delete(0, "end")

        self.sell_price.delete(0, "end")

        self.quantity.delete(0, "end")

        self.serial.delete(0, "end")