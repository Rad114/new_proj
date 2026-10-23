# ============================================================
# DASHBOARD.PY
# AI SQL STUDIO
# ============================================================

import tkinter as tk
from tkinter import messagebox
import os


# ============================================================
# COLORS
# ============================================================

BG_COLOR = "#101522"
SIDEBAR_COLOR = "#171D2B"
CARD_COLOR = "#1C2433"
INPUT_COLOR = "#252D3D"

ACCENT_COLOR = "#6C63E8"
HOVER_COLOR = "#7A72F5"

TEXT_COLOR = "#FFFFFF"
SECONDARY_TEXT = "#AAB2C0"

SUCCESS_COLOR = "#35D07F"
DANGER_COLOR = "#FF5C6C"
WARNING_COLOR = "#FFD166"


# ============================================================
# DASHBOARD
# ============================================================

class Dashboard:

    def __init__(self, root, user_name="User"):

        self.root = root
        self.user_name = user_name

        # ----------------------------------------------------
        # Current data source
        # ----------------------------------------------------

        self.db_path = None
        self.current_table = None

        # ----------------------------------------------------
        # Create dashboard
        # ----------------------------------------------------

        self.create_ui()

        # Show dashboard first
        self.show_dashboard()


    # ========================================================
    # CREATE UI
    # ========================================================

    def create_ui(self):

        # ----------------------------------------------------
        # Clear root
        # ----------------------------------------------------

        for widget in self.root.winfo_children():
            widget.destroy()


        self.root.configure(
            bg=BG_COLOR
        )


        # ====================================================
        # MAIN CONTAINER
        # ====================================================

        self.main_container = tk.Frame(
            self.root,
            bg=BG_COLOR
        )

        self.main_container.pack(
            fill="both",
            expand=True
        )


        # ====================================================
        # SIDEBAR
        # ====================================================

        self.sidebar = tk.Frame(
            self.main_container,
            bg=SIDEBAR_COLOR,
            width=245
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)


        # ====================================================
        # LOGO
        # ====================================================

        logo_frame = tk.Frame(
            self.sidebar,
            bg=SIDEBAR_COLOR
        )

        logo_frame.pack(
            fill="x",
            padx=20,
            pady=(25, 20)
        )


        tk.Label(
            logo_frame,
            text="⚡",
            font=("Segoe UI", 25),
            bg=SIDEBAR_COLOR,
            fg=ACCENT_COLOR
        ).pack(
            side="left"
        )


        logo_text = tk.Frame(
            logo_frame,
            bg=SIDEBAR_COLOR
        )

        logo_text.pack(
            side="left",
            padx=8
        )


        tk.Label(
            logo_text,
            text="AI SQL",
            font=("Segoe UI", 15, "bold"),
            bg=SIDEBAR_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w"
        )


        tk.Label(
            logo_text,
            text="STUDIO",
            font=("Segoe UI", 8, "bold"),
            bg=SIDEBAR_COLOR,
            fg=SECONDARY_TEXT
        ).pack(
            anchor="w"
        )


        # ====================================================
        # NAVIGATION LABEL
        # ====================================================

        tk.Label(
            self.sidebar,
            text="MAIN MENU",
            font=("Segoe UI", 8, "bold"),
            bg=SIDEBAR_COLOR,
            fg=SECONDARY_TEXT
        ).pack(
            anchor="w",
            padx=22,
            pady=(5, 8)
        )


        # ====================================================
        # NAVIGATION
        # ====================================================

        self.create_nav_button(
            "⌂",
            "Dashboard",
            self.show_dashboard
        )

        self.create_nav_button(
            "🗄",
            "Database Setup",
            self.show_database_setup
        )

        self.create_nav_button(
            "⚡",
            "AI SQL Generator",
            self.show_query_builder
        )

        self.create_nav_button(
            "📊",
            "Visualization",
            self.show_visualization
        )

        self.create_nav_button(
            "🧰",
            "Tool Explorer",
            self.show_tool_explorer
        )


        # ====================================================
        # DIVIDER
        # ====================================================

        tk.Frame(
            self.sidebar,
            bg="#2A3242",
            height=1
        ).pack(
            fill="x",
            padx=20,
            pady=15
        )


        tk.Label(
            self.sidebar,
            text="ACCOUNT",
            font=("Segoe UI", 8, "bold"),
            bg=SIDEBAR_COLOR,
            fg=SECONDARY_TEXT
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 8)
        )


        self.create_nav_button(
            "⚙",
            "Settings",
            self.show_settings
        )

        self.create_nav_button(
            "👤",
            "Account",
            self.show_account
        )


        # ====================================================
        # LOGOUT
        # ====================================================

        logout_button = tk.Button(
            self.sidebar,
            text="   ⇥   Logout",
            font=("Segoe UI", 10, "bold"),
            bg=SIDEBAR_COLOR,
            fg=DANGER_COLOR,
            activebackground="#242C3C",
            activeforeground=DANGER_COLOR,
            relief="flat",
            bd=0,
            cursor="hand2",
            anchor="w",
            padx=15,
            command=self.logout
        )

        logout_button.pack(
            fill="x",
            padx=12,
            pady=(15, 10),
            ipady=8
        )


        # ====================================================
        # CONTENT AREA
        # ====================================================

        self.content = tk.Frame(
            self.main_container,
            bg=BG_COLOR
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )


    # ========================================================
    # NAV BUTTON
    # ========================================================

    def create_nav_button(
        self,
        icon,
        text,
        command
    ):

        button = tk.Button(
            self.sidebar,
            text=f"  {icon}   {text}",
            font=("Segoe UI", 10),
            bg=SIDEBAR_COLOR,
            fg=SECONDARY_TEXT,
            activebackground="#242C3C",
            activeforeground=TEXT_COLOR,
            relief="flat",
            bd=0,
            cursor="hand2",
            anchor="w",
            padx=15,
            command=command
        )

        button.pack(
            fill="x",
            padx=12,
            pady=2,
            ipady=8
        )

        return button


    # ========================================================
    # CLEAR CONTENT
    # ========================================================

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()


    # ========================================================
    # DASHBOARD HOME
    # ========================================================

    def show_dashboard(self):

        self.clear_content()


        # ====================================================
        # HEADER
        # ====================================================

        header = tk.Frame(
            self.content,
            bg=BG_COLOR
        )

        header.pack(
            fill="x",
            padx=35,
            pady=(30, 15)
        )


        tk.Label(
            header,
            text=f"Welcome, {self.user_name}",
            font=("Segoe UI", 27, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w"
        )


        tk.Label(
            header,
            text="Your intelligent data analysis workspace",
            font=("Segoe UI", 10),
            bg=BG_COLOR,
            fg=SECONDARY_TEXT
        ).pack(
            anchor="w",
            pady=(5, 0)
        )


        # ====================================================
        # STAT CARDS
        # ====================================================

        stats_frame = tk.Frame(
            self.content,
            bg=BG_COLOR
        )

        stats_frame.pack(
            fill="x",
            padx=35,
            pady=10
        )


        self.create_stat_card(
            stats_frame,
            "🗄",
            "Data Source",
            self.get_database_name(),
            ACCENT_COLOR
        )


        self.create_stat_card(
            stats_frame,
            "📊",
            "Visualization",
            "Ready",
            SUCCESS_COLOR
        )


        self.create_stat_card(
            stats_frame,
            "⚡",
            "AI SQL",
            "Ollama",
            WARNING_COLOR
        )


        # ====================================================
        # HOW TO USE CARD
        # ====================================================

        how_card = tk.Frame(
            self.content,
            bg=CARD_COLOR
        )

        how_card.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(15, 30)
        )


        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        tk.Label(
            how_card,
            text="How to Use AI SQL Generator",
            font=("Segoe UI", 17, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w",
            padx=25,
            pady=(22, 5)
        )


        tk.Label(
            how_card,
            text="Follow these steps to analyze your data using natural language.",
            font=("Segoe UI", 9),
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 15)
        )


        # ====================================================
        # SCROLLABLE INSTRUCTIONS
        # ====================================================

        instruction_container = tk.Frame(
            how_card,
            bg=INPUT_COLOR
        )

        instruction_container.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 25)
        )


        instruction_canvas = tk.Canvas(
            instruction_container,
            bg=INPUT_COLOR,
            highlightthickness=0
        )

        instruction_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )


        instruction_scrollbar = tk.Scrollbar(
            instruction_container,
            orient="vertical",
            command=instruction_canvas.yview
        )

        instruction_scrollbar.pack(
            side="right",
            fill="y"
        )


        instruction_canvas.configure(
            yscrollcommand=instruction_scrollbar.set
        )


        instruction_inner = tk.Frame(
            instruction_canvas,
            bg=INPUT_COLOR
        )


        instruction_window = instruction_canvas.create_window(
            (0, 0),
            window=instruction_inner,
            anchor="nw"
        )


        def update_scroll_region(event=None):

            instruction_canvas.configure(
                scrollregion=instruction_canvas.bbox("all")
            )


        def resize_inner(event):

            instruction_canvas.itemconfig(
                instruction_window,
                width=event.width
            )


        instruction_inner.bind(
            "<Configure>",
            update_scroll_region
        )

        instruction_canvas.bind(
            "<Configure>",
            resize_inner
        )


        # ----------------------------------------------------
        # INSTRUCTIONS
        # ----------------------------------------------------

        self.create_instruction(
            instruction_inner,
            "01",
            "Select your data",
            "Open Database Setup and select your CSV, Excel, JSON or SQLite file."
        )


        self.create_instruction(
            instruction_inner,
            "02",
            "Check your data",
            "Database Setup shows the available tables, row count, duplicate rows and NULL values."
        )


        self.create_instruction(
            instruction_inner,
            "03",
            "Open AI SQL Generator",
            "Select AI SQL Generator from the left navigation menu."
        )


        self.create_instruction(
            instruction_inner,
            "04",
            "Select a table",
            "Choose the table that you want to analyze from the table dropdown."
        )


        self.create_instruction(
            instruction_inner,
            "05",
            "Ask a question",
            "Type a normal English question such as: Show the top 5 students by marks."
        )


        self.create_instruction(
            instruction_inner,
            "06",
            "Generate SQL",
            "Ollama converts your question into a read-only SQLite SELECT/WITH query."
        )


        self.create_instruction(
            instruction_inner,
            "07",
            "Review the result",
            "The generated SQL, AI explanation and database result are displayed on the screen."
        )


        self.create_instruction(
            instruction_inner,
            "08",
            "Visualize your result",
            "Use the Visualization page to create Bar, Line, Pie, Scatter, Area or Histogram charts."
        )



    # ========================================================
    # STAT CARD
    # ========================================================

    def create_stat_card(
        self,
        parent,
        icon,
        title,
        value,
        accent
    ):

        card = tk.Frame(
            parent,
            bg=CARD_COLOR,
            height=100
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        card.pack_propagate(False)


        tk.Label(
            card,
            text=icon,
            font=("Segoe UI", 22),
            bg=CARD_COLOR,
            fg=accent
        ).pack(
            side="left",
            padx=(20, 10)
        )


        text_frame = tk.Frame(
            card,
            bg=CARD_COLOR
        )

        text_frame.pack(
            side="left",
            anchor="center"
        )


        tk.Label(
            text_frame,
            text=title,
            font=("Segoe UI", 9),
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT
        ).pack(
            anchor="w"
        )


        tk.Label(
            text_frame,
            text=value,
            font=("Segoe UI", 12, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w",
            pady=(3, 0)
        )


    # ========================================================
    # INSTRUCTION ITEM
    # ========================================================

    def create_instruction(
        self,
        parent,
        number,
        title,
        description
    ):

        row = tk.Frame(
            parent,
            bg=INPUT_COLOR
        )

        row.pack(
            fill="x",
            padx=15,
            pady=10
        )


        number_label = tk.Label(
            row,
            text=number,
            font=("Segoe UI", 10, "bold"),
            bg=ACCENT_COLOR,
            fg=TEXT_COLOR,
            width=4,
            height=2
        )

        number_label.pack(
            side="left",
            padx=(5, 15)
        )


        text_frame = tk.Frame(
            row,
            bg=INPUT_COLOR
        )

        text_frame.pack(
            side="left",
            fill="x",
            expand=True
        )


        tk.Label(
            text_frame,
            text=title,
            font=("Segoe UI", 11, "bold"),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w"
        )


        tk.Label(
            text_frame,
            text=description,
            font=("Segoe UI", 9),
            bg=INPUT_COLOR,
            fg=SECONDARY_TEXT,
            wraplength=700,
            justify="left"
        ).pack(
            anchor="w",
            pady=(3, 0)
        )


    # ========================================================
    # DATABASE SETUP
    # ========================================================

    def show_database_setup(self):

        self.clear_content()

        try:

            from database_setup import DatabaseSetup

            DatabaseSetup(
                self.content
            )

        except Exception as error:

            messagebox.showerror(
                "Database Setup Error",
                str(error)
            )


    # ========================================================
    # AI SQL GENERATOR
    # ========================================================

    def show_query_builder(self):

        self.clear_content()

        try:

            from query_builder import QueryBuilder

            QueryBuilder(
                self.content,
                db_path=self.db_path,
                current_table=self.current_table
            )

        except Exception as error:

            messagebox.showerror(
                "AI SQL Generator Error",
                str(error)
            )


    # ========================================================
    # VISUALIZATION
    # ========================================================

    def show_visualization(self):

        self.clear_content()

        try:

            from visualization import Visualization

            # Try to pass database path if your
            # visualization class supports it.

            try:

                Visualization(
                    self.content,
                    db_path=self.db_path
                )

            except TypeError:

                # Fallback for Visualization(parent)

                Visualization(
                    self.content
                )

        except Exception as error:

            messagebox.showerror(
                "Visualization Error",
                str(error)
            )


    # ========================================================
    # TOOL EXPLORER
    # ========================================================

    def show_tool_explorer(self):

        self.clear_content()

        try:

            from tool_explorer import ToolExplorer

            ToolExplorer(
                self.content
            )

        except Exception as error:

            messagebox.showerror(
                "Tool Explorer Error",
                str(error)
            )


    # ========================================================
    # SQL HISTORY
    # ========================================================

    def show_history(self):

        self.clear_content()

        try:

            from history import History

            History(
                self.content
            )

        except Exception as error:

            messagebox.showerror(
                "SQL History Error",
                str(error)
            )


    # ========================================================
    # SETTINGS
    # ========================================================

    def show_settings(self):

        self.clear_content()

        try:

            from settings import Settings

            Settings(
                self.content
            )

        except Exception as error:

            messagebox.showerror(
                "Settings Error",
                str(error)
            )


    # ========================================================
    # ACCOUNT
    # ========================================================

    def show_account(self):

        self.clear_content()

        try:

            from account import Account

            Account(
                self.content
            )

        except Exception as error:

            messagebox.showerror(
                "Account Error",
                str(error)
            )


    # ========================================================
    # GET DATABASE NAME
    # ========================================================

    def get_database_name(self):

        if not self.db_path:
            return "No database"

        try:
            return os.path.basename(
                self.db_path
            )

        except Exception:
            return "Selected"


    # ========================================================
    # LOGOUT
    # ========================================================

    def logout(self):

        answer = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )

        if not answer:
            return


        self.root.destroy()


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.title(
        "AI SQL Studio"
    )

    root.geometry(
        "1400x850"
    )

    root.minsize(
        1100,
        700
    )

    root.configure(
        bg=BG_COLOR
    )


    Dashboard(
        root,
        user_name="Pratham"
    )


    root.mainloop()