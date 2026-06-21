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
