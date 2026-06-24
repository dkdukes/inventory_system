import customtkinter as ctk
from auth.session import Session


class Sidebar(ctk.CTkFrame):

    def __init__(self, parent, callback):

        super().__init__(parent, width=220)

        self.callback = callback
        self.buttons = {}
        self.active_button = None

        self.create_widgets()



    def create_widgets(self):

        # ---------------- LOGO ----------------
        logo_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        logo_frame.pack(
            pady=12
        )


        

        logo = ctk.CTkLabel(
            logo_frame,
            text="SHOP\nMANAGER",
            font=("Arial", 24, "bold"),
            justify="center"
        )

        logo.pack()
        

        version = ctk.CTkLabel(
            logo_frame,
            text="v1.0 ERP",
            font=("Arial", 11)
        )

        version.pack(
            pady=5
        )

    

        # ---------------- MENU ----------------
        menu = [
            "Dashboard",
            "Products",
            "Categories",
            "Suppliers",
            "Customers",
            "Sales",
            "Purchases",
            "Reports",
            "Settings"
        ]



        for item in menu:

            btn = ctk.CTkButton(
                self,
                text=item,
                height=40,
                fg_color="transparent",
                anchor="w",
                command=lambda i=item: self.set_active(i)
            )

            btn.pack(pady=6, padx=15, fill="x")

            self.buttons[item] = btn



        # ---------------- FOOTER ----------------
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(side="bottom", fill="x", pady=20)



        self.user_label = ctk.CTkLabel(
            footer,
            text=self.get_user_text(),
            font=("Arial", 14)
        )

        self.user_label.pack(pady=5)

    

        logout_btn = ctk.CTkButton(
            footer,
            text="Logout",
            fg_color="red",
            command=self.logout
        )

        logout_btn.pack(pady=5, padx=15, fill="x")

    def get_user_text(self):

        if Session.current_user:
            return f"{Session.current_user['name']} ({Session.current_user['role']})"

        return "Not Logged In"
    
    def refresh_user(self):

        self.user_label.configure(
            text=self.get_user_text()
        )

    # ---------------- ACTIVE STATE ----------------

    def set_active(self, item):

        # reset previous active
        if self.active_button:

            self.buttons[self.active_button].configure(
                fg_color="transparent"
            )



        # set new active
        self.active_button = item

        self.buttons[item].configure(
            fg_color="#1f6aa5"
        )



        # call page change
        self.callback(item)



    # ---------------- LOGOUT ----------------

    def logout(self):

        Session.current_user = None

        print("Logged out")

        # trigger full app reload
        self.callback("LOGOUT")