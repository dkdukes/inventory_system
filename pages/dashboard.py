import customtkinter as ctk
from database.db import Database


class Dashboard(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.db = Database()

        self.create_widgets()



    # ---------------- UI ----------------

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="Dashboard Overview",
            font=("Arial", 30, "bold")
        )

        title.pack(anchor="w", padx=20, pady=20)



        self.create_cards()
        self.create_bottom_sections()



    # ---------------- HELPERS ----------------

    def map_product(self, p):

        return {
            "id": p[0],
            "name": p[1],
            "category": p[2],
            "supplier": p[3],
            "buy_price": p[4],
            "sell_price": p[5],
            "quantity": p[6]
        }



    # ---------------- CARDS ----------------

    def create_cards(self):

        card_frame = ctk.CTkFrame(self)
        card_frame.pack(fill="x", padx=20)



        products = self.db.get_products()
        mapped = [self.map_product(p) for p in products]



        # METRICS

        total_products = len(mapped)

        total_units = sum(p["quantity"] for p in mapped)

        inventory_value = sum(
            p["quantity"] * p["sell_price"]
            for p in mapped
        )

        low_stock = len([
            p for p in mapped if p["quantity"] <= 5
        ])

        total_sales = self.db.get_total_sales()



        cards = [

            ("Total Products", total_products),

            ("Total Units", total_units),

            ("Inventory Value", f"${inventory_value:,.2f}"),

            ("Total Sales", f"${total_sales:,.2f}")

        ]



        for title, value in cards:

            card = ctk.CTkFrame(card_frame, width=200, height=120)

            card.pack(side="left", expand=True, fill="both", padx=10)



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



        # SALES PANEL (future charts area)

        sales = ctk.CTkFrame(bottom)

        sales.pack(side="left", expand=True, fill="both", padx=10)



        ctk.CTkLabel(
            sales,
            text="Sales Overview",
            font=("Arial", 20, "bold")
        ).pack(pady=20)



        ctk.CTkLabel(
            sales,
            text="Charts coming soon 📊"
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
        mapped = [self.map_product(p) for p in products]



        low_stock_items = [
            p for p in mapped if p["quantity"] <= 5
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
                    text=f"{p['name']} - {p['quantity']} left"
                ).pack(pady=5)