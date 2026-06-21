import customtkinter as ctk

from database.db import Database
from auth.session import Session
from tkinter import messagebox



class Sales(ctk.CTkFrame):


    def __init__(self,parent):

        super().__init__(parent)

        self.db = Database()

        self.create_ui()



    def create_ui(self):


        title = ctk.CTkLabel(
            self,
            text="Sales / POS",
            font=("Arial",30,"bold")
        )

        title.pack(pady=20)



        form = ctk.CTkFrame(self)

        form.pack(pady=20)



        self.customer = ctk.CTkEntry(
            form,
            placeholder_text="Customer Name",
            width=250
        )

        self.customer.grid(
            row=0,
            column=0,
            padx=10
        )



        self.product = ctk.CTkEntry(
            form,
            placeholder_text="Product ID",
            width=150
        )


        self.product.grid(
            row=0,
            column=1,
            padx=10
        )



        self.quantity = ctk.CTkEntry(
            form,
            placeholder_text="Quantity",
            width=150
        )


        self.quantity.grid(
            row=0,
            column=2,
            padx=10
        )



        button = ctk.CTkButton(
            form,
            text="Complete Sale",
            command=self.make_sale
        )


        button.grid(
            row=0,
            column=3,
            padx=10
        )
    
    
    def make_sale(self):


        try:

            customer = self.customer.get()

            product_id = int(
                self.product.get()
            )

            qty = int(
                self.quantity.get()
            )


            products = self.db.get_products()


            product = None


            for p in products:

                if p[0] == product_id:
                    product = p
                    break



            if not product:

                messagebox.showerror(
                    "Error",
                    "Product not found"
                )

                return



            if product[6] < qty:

                messagebox.showerror(
                    "Error",
                    "Insufficient stock"
                )

                return



            price = product[5]

            total = price * qty



            user_id = Session.current_user["id"]



            sale_id = self.db.create_sale(
                customer,
                total,
                user_id
            )



            self.db.add_sale_item(
                sale_id,
                product_id,
                qty,
                price
            )



            messagebox.showinfo(
                "Success",
                "Sale completed successfully"
            )


            self.clear()



        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )




    def clear(self):

        self.customer.delete(0,"end")
        self.product.delete(0,"end")
        self.quantity.delete(0,"end")