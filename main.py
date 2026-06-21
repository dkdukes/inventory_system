import customtkinter as ctk

from auth.login import Login
from pages.dashboard import Dashboard
from pages.products import Products
from auth.signup import Signup
from auth.session import Session
from pages.sales import Sales


class InventoryApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Inventory System")
        self.geometry("1200x700")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # MAIN CONTENT AREA
        self.content = ctk.CTkFrame(self)
        self.content.grid(row=0, column=1, sticky="nsew")

        self.sidebar = None

        self.pages = {
            "Dashboard": Dashboard,
            "Products": Products,
            "Sales" : Sales
        }

        self.show_login()



    # ---------------- AUTH FLOW ----------------

    def show_login(self):

        self.clear_all()

        login = Login(
            self.content,
            self.on_login_success
        )

        login.pack(expand=True, fill="both")



    def show_signup(self):

        self.clear_content()

        signup = Signup(
            self.content,
            on_success=self.show_login,
            go_to_login=self.show_login
        )

        signup.pack(expand=True, fill="both")



    def on_login_success(self):

        self.load_app()



    # ---------------- MAIN APP ----------------

    def load_app(self):

        self.clear_all()

        from components.sidebar import Sidebar

        self.sidebar = Sidebar(self, self.load_page)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.load_page("Dashboard")



    def load_page(self, page_name):

        # LOGOUT HANDLING
        if page_name == "LOGOUT":
            self.logout()
            return

        # SIGNUP HANDLING
        if page_name == "Signup":
            self.show_signup()
            return

        self.clear_content(keep_sidebar=True)

        Page = self.pages.get(page_name)

        if Page:

            page = Page(self.content)
            page.pack(fill="both", expand=True)



    # ---------------- LOGOUT ----------------

    def logout(self):

        Session.current_user = None

        if self.sidebar:
            self.sidebar.destroy()
            self.sidebar = None

        self.show_login()



    # ---------------- CLEANERS ----------------

    def clear_content(self, keep_sidebar=False):

        for widget in self.content.winfo_children():
            widget.destroy()



    def clear_all(self):

        self.clear_content()

        if self.sidebar:
            self.sidebar.destroy()
            self.sidebar = None



# ---------------- RUN APP ----------------

if __name__ == "__main__":

    app = InventoryApp()
    app.mainloop()