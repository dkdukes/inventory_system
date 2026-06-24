import customtkinter as ctk
from tkinter import messagebox

from database.auth_db import AuthDB
from auth.session import Session


class Login(ctk.CTkFrame):

    def __init__(self, parent, on_login_success):

        super().__init__(parent)

        self.db = AuthDB()
        self.on_login_success = on_login_success

        self.create_ui()



    # ================= UI =================

    def create_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Login",
            font=("Arial", 30, "bold")
        )

        title.pack(pady=30)



        form = ctk.CTkFrame(self)

        form.pack(pady=20)



        self.email = ctk.CTkEntry(
            form,
            placeholder_text="Email",
            width=300
        )

        self.email.pack(pady=10)



        self.password = ctk.CTkEntry(
            form,
            placeholder_text="Password",
            show="*",
            width=300
        )

        self.password.pack(pady=10)



        login_btn = ctk.CTkButton(
            form,
            text="Login",
            command=self.login
        )

        login_btn.pack(pady=15)



        signup_frame = ctk.CTkFrame(
            form,
            fg_color="transparent"
        )

        signup_frame.pack(pady=10)



        text = ctk.CTkLabel(
            signup_frame,
            text="Don't have an account?"
        )

        text.pack(side="left")



        signup_btn = ctk.CTkButton(
            signup_frame,
            text="Create Account",
            width=120,
            fg_color="transparent",
            text_color="blue",
            command=self.go_to_signup
        )

        signup_btn.pack(
            side="left",
            padx=10
        )



    # ================= LOGIN =================

    def login(self):

        email = self.email.get().strip()

        password = self.password.get().strip()



        if not email or not password:

            messagebox.showerror(
                "Error",
                "Please fill all fields"
            )

            return



        user = self.db.login_user(
            email,
            password
        )



        if user:

            # clear old session

            Session.current_user = None



            # create new session

            Session.current_user = {

                "id": user["id"],

                "name": user["full_name"],

                "role": user["role"]

            }



            messagebox.showinfo(
                "Success",
                f"Welcome {user['full_name']}"
            )



            self.on_login_success()



        else:

            messagebox.showerror(
                "Error",
                "Invalid email or password"
            )



    # ================= NAVIGATION =================

    def go_to_signup(self):

        root = self.winfo_toplevel()


        if hasattr(root, "show_signup"):

            root.show_signup()