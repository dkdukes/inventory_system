import customtkinter as ctk
from database.auth_db import AuthDB
from tkinter import messagebox


class Signup(ctk.CTkFrame):

    def __init__(self, parent, on_success=None, go_to_login=None):

        super().__init__(parent)

        self.db = AuthDB()
        self.on_success = on_success
        self.go_to_login = go_to_login

        self.create_ui()



    def create_ui(self):

        # ---------------- TITLE ----------------
        title = ctk.CTkLabel(
            self,
            text="Create Account",
            font=("Arial", 30, "bold")
        )
        title.pack(pady=20)



        # ---------------- FORM ----------------
        form = ctk.CTkFrame(self)
        form.pack(pady=20)



        self.full_name = ctk.CTkEntry(form, placeholder_text="Full Name", width=300)
        self.full_name.pack(pady=10)

        self.phone = ctk.CTkEntry(form, placeholder_text="Phone Number", width=300)
        self.phone.pack(pady=10)

        self.email = ctk.CTkEntry(form, placeholder_text="Email", width=300)
        self.email.pack(pady=10)

        self.password = ctk.CTkEntry(form, placeholder_text="Password", show="*", width=300)
        self.password.pack(pady=10)

        self.role = ctk.CTkComboBox(
            form,
            values=["admin", "staff"],
            width=300
        )
        self.role.set("staff")
        self.role.pack(pady=10)



        btn = ctk.CTkButton(
            form,
            text="Create Account",
            command=self.signup_user
        )
        btn.pack(pady=20)



        # ---------------- LOGIN LINK ----------------
        login_frame = ctk.CTkFrame(self, fg_color="transparent")
        login_frame.pack(pady=10)



        text = ctk.CTkLabel(
            login_frame,
            text="Already have an account?"
        )
        text.pack(side="left")



        login_btn = ctk.CTkButton(
            login_frame,
            text="Login",
            width=80,
            fg_color="transparent",
            text_color="blue",
            command=self.redirect_to_login
        )
        login_btn.pack(side="left", padx=10)



    # ---------------- SIGNUP LOGIC ----------------

    def signup_user(self):

        full_name = self.full_name.get()
        phone = self.phone.get()
        email = self.email.get()
        password = self.password.get()
        role = self.role.get()



        if not full_name or not email or not password:

            messagebox.showerror("Error", "Please fill required fields")
            return



        try:

            self.db.add_user(
                full_name,
                phone,
                email,
                password,
                role
            )

            messagebox.showinfo("Success", "Account created successfully!")

            self.clear_fields()

            if self.on_success:
                self.on_success()



        except Exception as e:

            messagebox.showerror("Error", str(e))



    # ---------------- UTILITIES ----------------

    def clear_fields(self):

        self.full_name.delete(0, "end")
        self.phone.delete(0, "end")
        self.email.delete(0, "end")
        self.password.delete(0, "end")



    def redirect_to_login(self):

        if self.go_to_login:
            self.go_to_login()