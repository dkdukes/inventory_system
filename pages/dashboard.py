import customtkinter as ctk
from database.db import Database


class Dashboard(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.db = Database()

        self.create_widgets()



    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="Dashboard Overview",
            font=("Arial", 30, "bold")
        )

        title.pack(anchor="w", padx=20, pady=20)



        self.create_cards()
        self.create_bottom_sections()



    # ---------------- CARDS ----------------

    def create_cards(self):

        card_frame = ctk.CTkFrame(self)
        card_frame.pack(fill="x", padx=20)



        # GET REAL DATA
        products = self.db.get_products()

        total_products = len(products)



        total_value = sum(
            p[6] * p[5] for p in products
        )  # quantity * sell_price



        low_stock = len(
            [p for p in products if p[6] <= 5]
        )



        cards = [

            ("Total Products", total_products),

            ("Low Stock Items", low_stock),

            ("Inventory Value", f"${total_value:,.2f}"),

            ("Total SKUs", len(products))

        ]



        for title, value in cards:

            card = ctk.CTkFrame(
                card_frame,
                width=200,
                height=120
            )

            card.pack(
                side="left",
                expand=True,
                fill="both",
                padx=10
            )



            ctk.CTkLabel(
                card,
                text=title,
                font=("Arial", 16)
            ).pack(pady=15)



            ctk.CTkLabel(
                card,
                text=value,
                font=("Arial", 28, "bold")
            ).pack()



    # ---------------- BOTTOM SECTION ----------------

    def create_bottom_sections(self):

        bottom = ctk.CTkFrame(self)
        bottom.pack(expand=True, fill="both", padx=20, pady=20)



        # SALES PANEL (placeholder for now)
        sales = ctk.CTkFrame(bottom)
        sales.pack(side="left", expand=True, fill="both", padx=10)



        ctk.CTkLabel(
            sales,
            text="Sales Overview",
            font=("Arial", 20, "bold")
        ).pack(pady=20)



        ctk.CTkLabel(
            sales,
            text="(Connect Sales module next)",
        ).pack()



        # LOW STOCK PANEL

        stock = ctk.CTkFrame(bottom)
        stock.pack(side="right", expand=True, fill="both", padx=10)



        ctk.CTkLabel(
            stock,
            text="Low Stock Alerts",
            font=("Arial", 20, "bold")
        ).pack(pady=20)



        products = self.db.get_products()

        low_stock_items = [
            p for p in products if p[6] <= 5
        ]



        if not low_stock_items:

            ctk.CTkLabel(
                stock,
                text="No low stock items 👍"
            ).pack()

        else:

            for p in low_stock_items:

                ctk.CTkLabel(
                    stock,
                    text=f"{p[1]} - {p[6]} left"
                ).pack(pady=5)