import customtkinter as ctk

from database.supplier_db import SupplierDB
from tkinter import messagebox



class Suppliers(ctk.CTkFrame):


    def __init__(self, parent):

        super().__init__(parent)


        self.db = SupplierDB()


        self.create_widgets()

        self.load_suppliers()



    # ================= UI =================

    def create_widgets(self):


        title = ctk.CTkLabel(
            self,
            text="Supplier Management",
            font=("Arial", 28, "bold")
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
            pady=5,
            fill="x"
        )



        self.phone = ctk.CTkEntry(
            form,
            placeholder_text="Phone Number"
        )

        self.phone.pack(
            pady=5,
            fill="x"
        )



        self.email = ctk.CTkEntry(
            form,
            placeholder_text="Email"
        )

        self.email.pack(
            pady=5,
            fill="x"
        )



        self.address = ctk.CTkEntry(
            form,
            placeholder_text="Address"
        )

        self.address.pack(
            pady=5,
            fill="x"
        )



        add = ctk.CTkButton(
            form,
            text="Add Supplier",
            command=self.add_supplier
        )


        add.pack(
            pady=10
        )



        # ================= TABLE =================


        self.table = ctk.CTkTextbox(
            self,
            font=("Arial", 14)
        )


        self.table.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=20
        )



    # ================= ADD SUPPLIER =================


    def add_supplier(self):


        name = self.name.get().strip()

        phone = self.phone.get().strip()

        email = self.email.get().strip()

        address = self.address.get().strip()



        if not name:

            messagebox.showerror(
                "Error",
                "Supplier name is required"
            )

            return



        self.db.add_supplier(

            name,

            phone,

            email,

            address

        )



        messagebox.showinfo(
            "Success",
            "Supplier added successfully"
        )



        self.clear_form()

        self.load_suppliers()



    # ================= LOAD SUPPLIERS =================


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
ID: {supplier["id"]}
Name: {supplier["name"]}
Phone: {supplier["phone"]}
Email: {supplier["email"]}
Address: {supplier["address"]}
Created: {supplier["created_at"]}

-----------------------------

"""

            )



    # ================= CLEAR FORM =================


    def clear_form(self):

        self.name.delete(
            0,
            "end"
        )

        self.phone.delete(
            0,
            "end"
        )

        self.email.delete(
            0,
            "end"
        )

        self.address.delete(
            0,
            "end"
        )