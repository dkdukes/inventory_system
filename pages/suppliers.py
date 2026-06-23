import customtkinter as ctk
from database.supplier_db import SupplierDB



class Suppliers(ctk.CTkFrame):


    def __init__(self,parent):

        super().__init__(parent)


        self.db = SupplierDB()


        self.create_widgets()

        self.load_suppliers()



    def create_widgets(self):


        title = ctk.CTkLabel(
            self,
            text="Supplier Management",
            font=("Arial",28,"bold")
        )


        title.pack(
            pady=20
        )



        form = ctk.CTkFrame(self)

        form.pack(
            padx=20,
            pady=10,
            fill="x"
        )



        self.name = ctk.CTkEntry(
            form,
            placeholder_text="Supplier Name"
        )

        self.name.pack(
            pady=5
        )



        self.phone = ctk.CTkEntry(
            form,
            placeholder_text="Phone Number"
        )

        self.phone.pack(
            pady=5
        )



        self.email = ctk.CTkEntry(
            form,
            placeholder_text="Email"
        )

        self.email.pack(
            pady=5
        )



        self.address = ctk.CTkEntry(
            form,
            placeholder_text="Address"
        )

        self.address.pack(
            pady=5
        )



        add = ctk.CTkButton(
            form,
            text="Add Supplier",
            command=self.add_supplier
        )


        add.pack(
            pady=10
        )



        self.table = ctk.CTkTextbox(
            self
        )


        self.table.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=20
        )




    def add_supplier(self):

        self.db.add_supplier(

            self.name.get(),

            self.phone.get(),

            self.email.get(),

            self.address.get()

        )


        self.load_suppliers()




    def load_suppliers(self):

        self.table.delete(
            "1.0",
            "end"
        )


        suppliers = self.db.get_suppliers()


        for supplier in suppliers:

            self.table.insert(
                "end",

                f"""
ID: {supplier[0]}
Name: {supplier[1]}
Phone: {supplier[2]}
Email: {supplier[3]}
Address: {supplier[4]}

----------------------

"""
            )