import tkinter as tk
from tkinter import ttk


# ============================================================
# COLORS
# ============================================================

BG_COLOR = "#101522"
SIDEBAR_COLOR = "#191D2B"
CARD_COLOR = "#202636"
CARD_HOVER = "#2A3042"
TEXT_COLOR = "#F5F5F5"
SECONDARY_TEXT = "#AEB5C5"
ACCENT_COLOR = "#6C63E8"
BORDER_COLOR = "#2C3243"


# ============================================================
# MAIN APPLICATION
# ============================================================

class AISQLGenerator:

    def __init__(self, root):

        self.root = root

        self.root.title("AI SQL Studio")

        # Full screen size
        self.root.geometry("1400x800")

        self.root.minsize(1100, 650)

        self.root.configure(
            bg=BG_COLOR
        )

        # Create the main layout
        self.create_layout()

        # Show default page
        self.show_query_builder()


    # ========================================================
    # MAIN LAYOUT
    # ========================================================

    def create_layout(self):

        # ----------------------------------------------------
        # SIDEBAR
        # ----------------------------------------------------

        self.sidebar = tk.Frame(
            self.root,
            bg=SIDEBAR_COLOR,
            width=245
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)


        # ----------------------------------------------------
        # CONTENT AREA
        # ----------------------------------------------------

        self.content = tk.Frame(
            self.root,
            bg=BG_COLOR
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )


        # Create sidebar
        self.create_sidebar()


    # ========================================================
    # SIDEBAR
    # ========================================================

    def create_sidebar(self):

        # ----------------------------------------------------
        # LOGO
        # ----------------------------------------------------

        logo_frame = tk.Frame(
            self.sidebar,
            bg=SIDEBAR_COLOR
        )

        logo_frame.pack(
            fill="x",
            padx=20,
            pady=(20, 35)
        )


        logo_icon = tk.Label(
            logo_frame,
            text="⚙",
            font=("Segoe UI", 25),
            bg=SIDEBAR_COLOR,
            fg=ACCENT_COLOR
        )

        logo_icon.pack(
            side="left"
        )


        logo_text = tk.Label(
            logo_frame,
            text=" SQL Studio",
            font=("Segoe UI", 21, "bold"),
            bg=SIDEBAR_COLOR,
            fg=ACCENT_COLOR
        )

        logo_text.pack(
            side="left"
        )


        # ----------------------------------------------------
        # MENU
        # ----------------------------------------------------

        self.menu_buttons = {}

        menu_items = [
            "Query Builder",
            "Database Setup",
            "Tool Explorer",
            "Dashboard",
            "History",
            "Help",
            "Settings",
            "Account"
        ]


        for item in menu_items:

            button = tk.Button(
                self.sidebar,
                text=item,
                font=("Segoe UI", 11),
                bg=SIDEBAR_COLOR,
                fg=SECONDARY_TEXT,
                activebackground=ACCENT_COLOR,
                activeforeground="white",
                bd=0,
                relief="flat",
                anchor="w",
                padx=20,
                cursor="hand2",
                command=lambda name=item:
                    self.menu_clicked(name)
            )

            button.pack(
                fill="x",
                padx=12,
                pady=3,
                ipady=9
            )

            self.menu_buttons[item] = button


        # ----------------------------------------------------
        # USER AREA
        # ----------------------------------------------------

        user_frame = tk.Frame(
            self.sidebar,
            bg="#202536"
        )

        user_frame.pack(
            side="bottom",
            fill="x",
            padx=12,
            pady=(10, 60)
        )


        # Avatar

        avatar = tk.Label(
            user_frame,
            text="P",
            font=("Segoe UI", 14, "bold"),
            bg=ACCENT_COLOR,
            fg="white",
            width=3,
            height=1
        )

        avatar.pack(
            side="left",
            padx=10,
            pady=10
        )


        # User name

        user_info = tk.Frame(
            user_frame,
            bg="#202536"
        )

        user_info.pack(
            side="left",
            pady=8
        )


        name_label = tk.Label(
            user_info,
            text="Pratham",
            font=("Segoe UI", 10, "bold"),
            bg="#202536",
            fg=TEXT_COLOR
        )

        name_label.pack(
            anchor="w"
        )


        role_label = tk.Label(
            user_info,
            text="AI SQL User",
            font=("Segoe UI", 8),
            bg="#202536",
            fg=SECONDARY_TEXT
        )

        role_label.pack(
            anchor="w"
        )


        # ----------------------------------------------------
        # LOGOUT BUTTON
        # ----------------------------------------------------

        logout_button = tk.Button(
            self.sidebar,
            text="↪  Logout",
            font=("Segoe UI", 10),
            bg="#3A4053",
            fg="white",
            activebackground="#4A5065",
            activeforeground="white",
            bd=0,
            relief="flat",
            cursor="hand2"
        )

        logout_button.pack(
            side="bottom",
            fill="x",
            padx=12,
            pady=(0, 15),
            ipady=8
        )


    # ========================================================
    # MENU CLICK
    # ========================================================

    def menu_clicked(self, name):

        if name == "Query Builder":

            self.show_query_builder()

        else:

            self.show_placeholder(name)


    # ========================================================
    # CLEAR CONTENT
    # ========================================================

    def clear_content(self):

        for widget in self.content.winfo_children():

            widget.destroy()


    # ========================================================
    # QUERY BUILDER PAGE
    # ========================================================

    def show_query_builder(self):

        self.clear_content()

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        title = tk.Label(
            self.content,
            text="Query Builder",
            font=("Segoe UI", 27, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )

        title.pack(
            anchor="w",
            padx=32,
            pady=(28, 20)
        )


        # ----------------------------------------------------
        # TOOL LABEL
        # ----------------------------------------------------

        tool_label = tk.Label(
            self.content,
            text="Select a Tool:",
            font=("Segoe UI", 15, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )

        tool_label.pack(
            anchor="w",
            padx=32
        )


        # ----------------------------------------------------
        # TOOL DROPDOWN
        # ----------------------------------------------------

        self.tool_combo = ttk.Combobox(
            self.content,
            values=[
                "Generate SQL",
                "Explain SQL",
                "Optimize SQL"
            ],
            state="readonly",
            font=("Segoe UI", 11)
        )

        self.tool_combo.set(
            "Generate SQL"
        )

        self.tool_combo.pack(
            anchor="w",
            padx=32,
            pady=(8, 25),
            ipadx=100,
            ipady=6
        )


        # ----------------------------------------------------
        # DATABASE LABEL
        # ----------------------------------------------------

        database_label = tk.Label(
            self.content,
            text="Select a Database:",
            font=("Segoe UI", 15, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )

        database_label.pack(
            anchor="w",
            padx=32
        )


        # ----------------------------------------------------
        # DATABASE DROPDOWN
        # ----------------------------------------------------

        self.database_combo = ttk.Combobox(
            self.content,
            values=[
                "sales.db (SQLite)"
            ],
            state="readonly",
            font=("Segoe UI", 11)
        )

        self.database_combo.set(
            "sales.db (SQLite)"
        )

        self.database_combo.pack(
            anchor="w",
            padx=32,
            pady=(8, 25),
            ipadx=100,
            ipady=6
        )


        # ----------------------------------------------------
        # TABLE AREA
        # ----------------------------------------------------

        table_area = tk.Frame(
            self.content,
            bg=BG_COLOR
        )

        table_area.pack(
            fill="x",
            padx=32
        )


        # ----------------------------------------------------
        # LEFT CARD
        # ----------------------------------------------------

        left_card = tk.Frame(
            table_area,
            bg=CARD_COLOR
        )

        left_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 12)
        )


        left_title = tk.Label(
            left_card,
            text="Select Tables",
            font=("Segoe UI", 14, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )

        left_title.pack(
            anchor="w",
            padx=15,
            pady=(15, 10)
        )


        # Search box

        self.search_entry = tk.Entry(
            left_card,
            font=("Segoe UI", 11),
            bg="#F0F2FA",
            fg="#202020",
            relief="flat"
        )

        self.search_entry.insert(
            0,
            "Search tables..."
        )

        self.search_entry.pack(
            fill="x",
            padx=15,
            ipady=8
        )


        # Table list

        self.table_list = tk.Listbox(
            left_card,
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            selectbackground=ACCENT_COLOR,
            selectforeground="white",
            font=("Segoe UI", 11),
            bd=0,
            highlightthickness=0
        )

        self.table_list.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )


        # Demo tables for now

        demo_tables = [
            "🗄  customers          4 cols",
            "🗄  products           4 cols",
            "🗄  orders             6 cols",
            "🗄  employees          5 cols"
        ]

        for table in demo_tables:

            self.table_list.insert(
                "end",
                table
            )


        # ----------------------------------------------------
        # RIGHT CARD
        # ----------------------------------------------------

        right_card = tk.Frame(
            table_area,
            bg=CARD_COLOR
        )

        right_card.pack(
            side="right",
            fill="both",
            expand=True
        )


        right_title = tk.Label(
            right_card,
            text="Selected Tables",
            font=("Segoe UI", 14, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )

        right_title.pack(
            anchor="w",
            padx=15,
            pady=(15, 10)
        )


        self.selected_text = tk.Text(
            right_card,
            height=10,
            bg="#252B3B",
            fg=SECONDARY_TEXT,
            insertbackground="white",
            font=("Segoe UI", 10),
            bd=0,
            relief="flat",
            wrap="word"
        )

        self.selected_text.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.selected_text.insert(
            "1.0",
            "Select a table from the left panel."
        )

        self.selected_text.config(
            state="disabled"
        )


        # ----------------------------------------------------
        # GENERATE SQL CARD
        # ----------------------------------------------------

        sql_card = tk.Frame(
            self.content,
            bg=CARD_COLOR
        )

        sql_card.pack(
            fill="both",
            expand=True,
            padx=32,
            pady=25
        )


        sql_title = tk.Label(
            sql_card,
            text="Generate SQL",
            font=("Segoe UI", 24, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )

        sql_title.pack(
            anchor="w",
            padx=22,
            pady=(18, 5)
        )


        # Small accent line

        line = tk.Frame(
            sql_card,
            bg=ACCENT_COLOR,
            height=4,
            width=40
        )

        line.pack(
            anchor="w",
            padx=22,
            pady=(0, 15)
        )


        query_label = tk.Label(
            sql_card,
            text="Describe your query in natural language:",
            font=("Segoe UI", 13, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )

        query_label.pack(
            anchor="w",
            padx=22
        )


        # Query input

        self.query_text = tk.Text(
            sql_card,
            height=5,
            bg="#151A27",
            fg=TEXT_COLOR,
            insertbackground="white",
            font=("Segoe UI", 11),
            bd=0,
            relief="flat",
            wrap="word"
        )

        self.query_text.pack(
            fill="x",
            padx=22,
            pady=12
        )


        self.query_text.insert(
            "1.0",
            "Example: Show the top 5 products by revenue"
        )


        # Generate button

        generate_button = tk.Button(
            sql_card,
            text="🚀  Generate SQL",
            font=("Segoe UI", 11, "bold"),
            bg=ACCENT_COLOR,
            fg="white",
            activebackground="#7A72F5",
            activeforeground="white",
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self.generate_sql
        )

        generate_button.pack(
            anchor="e",
            padx=22,
            pady=(0, 15),
            ipadx=15,
            ipady=7
        )


    # ========================================================
    # GENERATE SQL
    # ========================================================

    def generate_sql(self):

        question = self.query_text.get(
            "1.0",
            "end"
        ).strip()


        if not question:

            return


        # Clear old SQL area if it exists

        for widget in self.content.winfo_children():

            pass


        # Show result window

        result_window = tk.Toplevel(
            self.root
        )

        result_window.title(
            "Generated SQL"
        )

        result_window.geometry(
            "750x500"
        )

        result_window.configure(
            bg=BG_COLOR
        )


        title = tk.Label(
            result_window,
            text="Generated SQL",
            font=("Segoe UI", 20, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )

        title.pack(
            anchor="w",
            padx=25,
            pady=20
        )


        sql_box = tk.Text(
            result_window,
            bg="#151A27",
            fg="#8EE6A8",
            font=("Consolas", 11),
            bd=0,
            wrap="word"
        )

        sql_box.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )


        # Demo SQL for now

        sql = """
SELECT
    p.product_name,
    SUM(o.amount) AS revenue
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
GROUP BY p.product_name
ORDER BY revenue DESC
LIMIT 5;
"""


        sql_box.insert(
            "1.0",
            sql
        )


        sql_box.config(
            state="disabled"
        )


        execute_button = tk.Button(
            result_window,
            text="Execute Query",
            font=("Segoe UI", 11, "bold"),
            bg=ACCENT_COLOR,
            fg="white",
            bd=0,
            cursor="hand2"
        )

        execute_button.pack(
            pady=20,
            ipadx=20,
            ipady=8
        )


    # ========================================================
    # PLACEHOLDER PAGES
    # ========================================================

    def show_placeholder(self, page_name):

        self.clear_content()

        title = tk.Label(
            self.content,
            text=page_name,
            font=("Segoe UI", 28, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )

        title.pack(
            anchor="w",
            padx=32,
            pady=30
        )


        message = tk.Label(
            self.content,
            text=f"{page_name} page will be added in the next step.",
            font=("Segoe UI", 14),
            bg=BG_COLOR,
            fg=SECONDARY_TEXT
        )

        message.pack(
            anchor="w",
            padx=32
        )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = AISQLGenerator(root)

    root.mainloop()