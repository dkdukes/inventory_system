import customtkinter as ctk

from database.product_db import ProductDB
from auth.session import Session
from tkinter import messagebox

import os
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas



class Sales(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.db = ProductDB()

        self.cart = []

        self.create_ui()



    # ================= UI =================

    def create_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Point Of Sale",
            font=("Arial",30,"bold")
        )

        title.pack(pady=20)



        customer_frame = ctk.CTkFrame(self)
        customer_frame.pack(pady=10)


        ctk.CTkLabel(
            customer_frame,
            text="Customer Name"
        ).pack(side="left", padx=10)



        self.customer = ctk.CTkEntry(
            customer_frame,
            width=300,
            placeholder_text="Optional"
        )

        self.customer.pack(side="left")



        # SEARCH

        search_frame = ctk.CTkFrame(self)

        search_frame.pack(
            fill="x",
            padx=20
        )


        self.search = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search product..."
        )

        self.search.pack(
            side="left",
            padx=10
        )



        ctk.CTkButton(
            search_frame,
            text="Search",
            command=self.search_product
        ).pack(
            side="left"
        )



        # PRODUCTS

        self.product_list = ctk.CTkScrollableFrame(
            self,
            height=150
        )

        self.product_list.pack(
            fill="x",
            padx=20,
            pady=10
        )



        ctk.CTkLabel(
            self,
            text="Cart",
            font=("Arial",20,"bold")
        ).pack()



        self.cart_frame = ctk.CTkScrollableFrame(self)

        self.cart_frame.pack(
            expand=True,
            fill="both",
            padx=20
        )



        self.total_label = ctk.CTkLabel(
            self,
            text="Total: Ksh0",
            font=("Arial",22,"bold")
        )

        self.total_label.pack(pady=10)



        ctk.CTkButton(
            self,
            text="Complete Sale",
            command=self.checkout
        ).pack(pady=5)



        ctk.CTkButton(
            self,
            text="Clear Cart",
            fg_color="gray",
            command=self.clear_cart
        ).pack(pady=5)



    # ================= SEARCH =================

    def search_product(self):

        for widget in self.product_list.winfo_children():

            widget.destroy()



        products = self.db.search_products(
            self.search.get()
        )



        for product in products:


            row = ctk.CTkFrame(
                self.product_list
            )

            row.pack(
                fill="x",
                pady=5
            )



            text = (
                f"{product['name']} | "
                f"Price: {product['sell_price']} | "
                f"Stock: {product['quantity']}"
            )



            ctk.CTkLabel(
                row,
                text=text
            ).pack(
                side="left",
                padx=10
            )



            ctk.CTkButton(
                row,
                text="Add",
                width=80,
                command=lambda p=product:self.add_cart(p)
            ).pack(
                side="right"
            )



    # ================= CART =================

    def add_cart(self, product):

        for item in self.cart:


            if item["id"] == product["id"]:


                if item["qty"] >= product["quantity"]:

                    messagebox.showwarning(
                        "Stock Limit",
                        "No more stock available"
                    )

                    return



                item["qty"] += 1

                self.refresh_cart()

                return




        self.cart.append({

            "id": product["id"],

            "name": product["name"],

            "price": product["sell_price"],

            "qty": 1,

            "stock": product["quantity"]

        })


        self.refresh_cart()



    def refresh_cart(self):


        for widget in self.cart_frame.winfo_children():

            widget.destroy()



        total = 0



        for index,item in enumerate(self.cart):


            amount = item["qty"] * item["price"]

            total += amount



            row = ctk.CTkFrame(
                self.cart_frame
            )

            row.pack(
                fill="x",
                pady=5
            )



            ctk.CTkLabel(
                row,
                text=item["name"]
            ).pack(
                side="left",
                padx=10
            )



            ctk.CTkButton(
                row,
                text="-",
                width=40,
                command=lambda i=index:self.decrease_quantity(i)
            ).pack(
                side="left"
            )



            ctk.CTkLabel(
                row,
                text=str(item["qty"])
            ).pack(
                side="left"
            )



            ctk.CTkButton(
                row,
                text="+",
                width=40,
                command=lambda i=index:self.increase_quantity(i)
            ).pack(
                side="left"
            )



            ctk.CTkLabel(
                row,
                text=f"Ksh{amount}"
            ).pack(
                side="right",
                padx=20
            )



            ctk.CTkButton(
                row,
                text="Remove",
                fg_color="red",
                command=lambda i=index:self.remove_item(i)
            ).pack(
                side="right"
            )



        self.total_label.configure(
            text=f"Total: Ksh{total}"
        )



    def remove_item(self,index):

        self.cart.pop(index)

        self.refresh_cart()



    def increase_quantity(self,index):

        item = self.cart[index]


        if item["qty"] >= item["stock"]:

            messagebox.showwarning(
                "Stock Limit",
                "Maximum available stock reached"
            )

            return


        item["qty"] += 1

        self.refresh_cart()



    def decrease_quantity(self,index):

        item = self.cart[index]


        item["qty"] -= 1


        if item["qty"] <= 0:

            self.cart.pop(index)


        self.refresh_cart()



    def clear_cart(self):

        self.cart.clear()

        self.refresh_cart()



    # ================= CHECKOUT =================


    def checkout(self):

        if not self.cart:

            messagebox.showerror(
                "Error",
                "Cart is empty"
            )

            return



        total = sum(
            item["qty"] * item["price"]
            for item in self.cart
        )



        sale_id = self.db.create_sale(

            self.customer.get(),

            total,

            Session.current_user["id"]

        )



        for item in self.cart:


            self.db.add_sale_item(

                sale_id,

                item["id"],

                item["qty"],

                item["price"]

            )



        self.generate_receipt(
            sale_id,
            total
        )



        messagebox.showinfo(
            "Success",
            "Sale completed"
        )


        self.cart.clear()

        self.refresh_cart()



    # ================= RECEIPT =================


    def generate_receipt(
        self,
        sale_id,
        total
    ):


        if not os.path.exists("receipts"):

            os.makedirs("receipts")



        filename = f"receipts/receipt_{sale_id}.pdf"



        c = canvas.Canvas(
            filename,
            pagesize=A4
        )



        c.drawString(
            200,
            800,
            "INVENTORY PRO RECEIPT"
        )


        c.drawString(
            50,
            760,
            f"Sale ID: {sale_id}"
        )


        c.drawString(
            50,
            740,
            f"Customer: {self.customer.get()}"
        )


        c.drawString(
            50,
            720,
            f"Date: {datetime.now()}"
        )


        y = 680


        for item in self.cart:


            c.drawString(
                60,
                y,
                f"{item['name']} x {item['qty']} = {item['qty']*item['price']}"
            )

            y -= 20



        c.drawString(
            50,
            y-20,
            f"TOTAL: {total}"
        )



        c.save()