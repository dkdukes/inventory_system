import customtkinter as ctk

from database.db import Database
from auth.session import Session
from tkinter import messagebox


class Sales(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.db = Database()

        self.cart = []

        self.create_ui()



    def create_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Point Of Sale",
            font=("Arial",30,"bold")
        )

        title.pack(pady=20)



        # CUSTOMER

        self.customer = ctk.CTkEntry(
            self,
            placeholder_text="Customer Name",
            width=300
        )

        self.customer.pack(pady=10)



        # PRODUCT SEARCH

        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill="x", padx=20)



        self.search = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search product..."
        )

        self.search.pack(
            side="left",
            padx=10
        )


        search_btn = ctk.CTkButton(
            search_frame,
            text="Search",
            command=self.search_product
        )

        search_btn.pack(
            side="left"
        )



        # PRODUCT LIST

        self.product_list = ctk.CTkScrollableFrame(
            self,
            height=150
        )

        self.product_list.pack(
            fill="x",
            padx=20,
            pady=10
        )



        # CART

        ctk.CTkLabel(
            self,
            text="Cart",
            font=("Arial",20,"bold")
        ).pack()



        self.cart_frame = ctk.CTkScrollableFrame(
            self
        )

        self.cart_frame.pack(
            expand=True,
            fill="both",
            padx=20
        )



        self.total_label = ctk.CTkLabel(
            self,
            text="Total: $0",
            font=("Arial",22,"bold")
        )

        self.total_label.pack(
            pady=10
        )



        checkout = ctk.CTkButton(
            self,
            text="Complete Sale",
            command=self.checkout
        )

        checkout.pack(
            pady=10
        )


    

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
                f"{product[1]} | "
                f"Price: ${product[2]} | "
                f"Available: {product[3]}"
            )


            ctk.CTkLabel(
                row,
                text=text
            ).pack(
                side="left",
                padx=10
            )



            btn = ctk.CTkButton(
                row,
                text="Add",
                width=80,
                command=lambda p=product:self.add_cart(p)
            )


            btn.pack(
                side="right"
            )

    



    def add_cart(self, product):

        product_id = product[0]

        available_stock = product[3]


        # Check if already in cart
        for item in self.cart:

            if item["id"] == product_id:


                if item["qty"] >= available_stock:

                    messagebox.showwarning(
                        "Stock Limit",
                        f"Only {available_stock} items available"
                    )

                    return



                item["qty"] += 1

                self.refresh_cart()

                return



        # Add new item

        self.cart.append({

            "id": product[0],
            "name": product[1],
            "price": product[2],
            "qty": 1,
            "stock": product[3]

        })


        self.refresh_cart()



    

    def refresh_cart(self):

        # clear cart display
        for widget in self.cart_frame.winfo_children():
            widget.destroy()


        total = 0


        for index, item in enumerate(self.cart):


            amount = item["price"] * item["qty"]

            total += amount



            row = ctk.CTkFrame(
                self.cart_frame
            )

            row.pack(
                fill="x",
                pady=5
            )



            # PRODUCT NAME

            name = ctk.CTkLabel(
                row,
                text=item["name"],
                width=180
            )

            name.pack(
                side="left",
                padx=10
            )



            # MINUS BUTTON

            minus = ctk.CTkButton(
                row,
                text="-",
                width=40,
                command=lambda i=index:self.decrease_quantity(i)
            )

            minus.pack(
                side="left"
            )



            # QUANTITY

            qty = ctk.CTkLabel(
                row,
                text=str(item["qty"]),
                width=50,
                font=("Arial",16,"bold")
            )

            qty.pack(
                side="left"
            )



            # PLUS BUTTON

            plus = ctk.CTkButton(
                row,
                text="+",
                width=40,
                command=lambda i=index:self.increase_quantity(i)
            )


            plus.pack(
                side="left"
            )



            # PRICE

            price = ctk.CTkLabel(
                row,
                text=f"${amount}",
                width=100
            )

            price.pack(
                side="right",
                padx=20
            )



        self.total_label.configure(
            text=f"Total: ${total}"
        )



    def increase_quantity(self,index):

        item = self.cart[index]


        # STOCK CHECK

        if item["qty"] >= item["stock"]:


            messagebox.showwarning(
                "Stock Limit",
                f"Only {item['stock']} units available"
            )

            return



        item["qty"] += 1


        self.refresh_cart()
    

    def decrease_quantity(self,index):

        item = self.cart[index]


        item["qty"] -= 1



        # remove item if quantity becomes zero

        if item["qty"] <= 0:

            self.cart.pop(index)



        self.refresh_cart()




    def checkout(self):

        if not self.cart:

            messagebox.showerror(
                "Error",
                "Cart is empty"
            )

            return



        # FINAL STOCK VALIDATION

        products = self.db.get_products()


        for item in self.cart:

            for product in products:


                if product[0] == item["id"]:


                    if item["qty"] > product[6]:

                        messagebox.showerror(
                            "Stock Error",
                            f"{item['name']} does not have enough stock"
                        )

                        return


        self.cart.clear()

        self.refresh_cart()