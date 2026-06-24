import customtkinter as ctk
from database.product_db import ProductDB


class Dashboard(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.db = ProductDB()

        self.create_widgets()



    # ---------------- UI ----------------

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="Dashboard Overview",
            font=("Arial", 30, "bold")
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=20
        )


        self.create_cards()
        self.create_bottom_sections()



    # ---------------- HELPERS ----------------

    def map_product(self, p):

        return {
            "id": p["id"],

            "name": p["name"],

            "category": p.get(
                "category_name",
                "N/A"
            ),

            "supplier": p.get(
                "supplier_name",
                "N/A"
            ),

            "buy_price": float(
                p["buy_price"] or 0
            ),

            "sell_price": float(
                p["sell_price"] or 0
            ),

            "quantity": int(
                p["quantity"] or 0
            )
        }



    # ---------------- CARDS ----------------

    def create_cards(self):

        card_frame = ctk.CTkFrame(self)

        card_frame.pack(
            fill="x",
            padx=20
        )


        products = self.db.get_products()

        mapped = [
            self.map_product(p)
            for p in products
        ]



        total_products = len(mapped)


        total_units = sum(
            p["quantity"]
            for p in mapped
        )


        inventory_value = sum(
            p["quantity"] *
            p["sell_price"]

            for p in mapped
        )


        total_sales = self.db.get_total_sales()



        cards = [

            (
                "Total Products",
                total_products
            ),

            (
                "Total Units",
                total_units
            ),

            (
                "Inventory Value",
                f"Ksh{inventory_value:,.2f}"
            ),

            (
                "Total Sales",
                f"Ksh{total_sales:,.2f}"
            )

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
                font=("Arial",16)
            ).pack(
                pady=15
            )



            ctk.CTkLabel(
                card,
                text=str(value),
                font=("Arial",28,"bold")
            ).pack()



    # ---------------- BOTTOM SECTION ----------------

    def create_bottom_sections(self):


        bottom = ctk.CTkFrame(self)


        bottom.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=20
        )



        # ================= SALES =================

        sales = ctk.CTkFrame(bottom)


        sales.pack(
            side="left",
            expand=True,
            fill="both",
            padx=10
        )



        ctk.CTkLabel(
            sales,
            text="Sales Overview",
            font=("Arial",20,"bold")
        ).pack(
            pady=20
        )



        today_sales = self.db.get_today_sales()



        ctk.CTkLabel(
            sales,
            text=f"Today's Sales: Ksh{today_sales:,.2f}",
            font=("Arial",16)
        ).pack()



        ctk.CTkLabel(
            sales,
            text="Charts coming soon"
        ).pack(
            pady=20
        )



        # ================= LOW STOCK =================


        stock = ctk.CTkFrame(bottom)


        stock.pack(
            side="right",
            expand=True,
            fill="both",
            padx=10
        )



        ctk.CTkLabel(
            stock,
            text="Low Stock Alerts",
            font=("Arial",20,"bold")
        ).pack(
            pady=20
        )



        products = self.db.get_products()


        mapped = [
            self.map_product(p)
            for p in products
        ]



        low_stock_items = [

            p for p in mapped

            if p["quantity"] <= 5

        ]



        if not low_stock_items:


            ctk.CTkLabel(
                stock,
                text="No low stock items"
            ).pack()



        else:


            for p in low_stock_items:


                ctk.CTkLabel(
                    stock,

                    text=(
                        f"{p['name']} "
                        f"- {p['quantity']} left"
                    )

                ).pack(
                    pady=5
                )