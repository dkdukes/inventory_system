import customtkinter as ctk
from database.category_db import CategoryDB



class Categories(ctk.CTkFrame):


    def __init__(self,parent):

        super().__init__(parent)


        self.db = CategoryDB()


        self.create_widgets()

        self.load_categories()



    def create_widgets(self):


        title = ctk.CTkLabel(
            self,
            text="Category Management",
            font=("Arial",28,"bold")
        )

        title.pack(
            pady=20
        )



        # INPUT FRAME

        form = ctk.CTkFrame(self)

        form.pack(
            pady=10,
            padx=20,
            fill="x"
        )


        self.name_entry = ctk.CTkEntry(
            form,
            placeholder_text="Category Name"
        )

        self.name_entry.pack(
            pady=10,
            padx=10
        )



        self.description_entry = ctk.CTkEntry(
            form,
            placeholder_text="Description"
        )

        self.description_entry.pack(
            pady=10,
            padx=10
        )



        add_btn = ctk.CTkButton(
            form,
            text="Add Category",
            command=self.add_category
        )

        add_btn.pack(
            pady=10
        )



        # LIST


        self.category_list = ctk.CTkTextbox(
            self,
            height=300
        )


        self.category_list.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )



    def load_categories(self):

        self.category_list.delete(
            "1.0",
            "end"
        )


        categories = self.db.get_categories()


        for cat in categories:

            self.category_list.insert(
                "end",
                f"{cat[0]} | {cat[1]} | {cat[2]}\n"
            )




    def add_category(self):

        name = self.name_entry.get()

        description = self.description_entry.get()


        if name:

            self.db.add_category(
                name,
                description
            )


            self.load_categories()


            self.name_entry.delete(
                0,
                "end"
            )

            self.description_entry.delete(
                0,
                "end"
            )