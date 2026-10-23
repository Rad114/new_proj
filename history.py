# ============================================================
# HISTORY.PY
# AI SQL STUDIO
#
# Stores:
#   • Executed SQL Queries
#   • Query Results
#   • Visualized Charts
#   • Database Name
#   • User Question
#   • Date / Time
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os


# ============================================================
# COLORS
# ============================================================

BG_COLOR = "#101522"
SIDEBAR_COLOR = "#171D2B"
CARD_COLOR = "#1C2433"
INPUT_COLOR = "#252D3D"

TEXT_COLOR = "#FFFFFF"
SECONDARY_TEXT = "#AAB2C0"

ACCENT_COLOR = "#6C63E8"
HOVER_COLOR = "#7A72F5"

SUCCESS_COLOR = "#35D07F"
DANGER_COLOR = "#FF5C6C"
WARNING_COLOR = "#FFD166"


# ============================================================
# HISTORY DATABASE
# ============================================================

HISTORY_DB = "sql_history.db"


# ============================================================
# SQL HISTORY
# ============================================================

class SQLHistory:

    def __init__(self, parent):

        self.parent = parent

        self.history_data = []

        self.create_history_database()

        self.create_ui()

        self.load_history()


    # ========================================================
    # CREATE HISTORY DATABASE
    # ========================================================

    def create_history_database(self):

        try:

            connection = sqlite3.connect(
                HISTORY_DB
            )

            cursor = connection.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date_time TEXT NOT NULL,
                    database_name TEXT,
                    question TEXT,
                    sql_query TEXT,
                    rows_returned INTEGER DEFAULT 0,
                    action_type TEXT DEFAULT 'QUERY',
                    chart_type TEXT DEFAULT ''
                )
                """
            )

            connection.commit()

            connection.close()


        except Exception as error:

            messagebox.showerror(
                "History Database Error",
                str(error)
            )


    # ========================================================
    # CREATE UI
    # ========================================================

    def create_ui(self):

        # ----------------------------------------------------
        # CLEAR PARENT
        # ----------------------------------------------------

        for widget in self.parent.winfo_children():

            widget.destroy()


        # ====================================================
        # MAIN
        # ====================================================

        main = tk.Frame(
            self.parent,
            bg=BG_COLOR
        )

        main.pack(
            fill="both",
            expand=True
        )


        # ====================================================
        # HEADER
        # ====================================================

        header = tk.Frame(
            main,
            bg=BG_COLOR
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(25, 10)
        )


        tk.Label(
            header,
            text="SQL History",
            font=("Segoe UI", 26, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w"
        )


        tk.Label(
            header,
            text=(
                "View previously executed SQL queries "
                "and visualizations."
            ),
            font=("Segoe UI", 10),
            bg=BG_COLOR,
            fg=SECONDARY_TEXT
        ).pack(
            anchor="w",
            pady=(5, 0)
        )


        # ====================================================
        # TOOLBAR
        # ====================================================

        toolbar = tk.Frame(
            main,
            bg=CARD_COLOR
        )

        toolbar.pack(
            fill="x",
            padx=30,
            pady=12
        )


        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        tk.Label(
            toolbar,
            text="Search",
            font=("Segoe UI", 9, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            side="left",
            padx=(15, 8)
        )


        self.search_var = tk.StringVar()


        self.search_entry = tk.Entry(
            toolbar,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            relief="flat",
            bd=0
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5,
            ipady=8
        )


        self.search_var.trace_add(
            "write",
            lambda *args: self.search_history()
        )


        # ----------------------------------------------------
        # FILTER
        # ----------------------------------------------------

        tk.Label(
            toolbar,
            text="Type",
            font=("Segoe UI", 9, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            side="left",
            padx=(15, 8)
        )


        self.filter_var = tk.StringVar(
            value="All"
        )


        self.filter_combo = ttk.Combobox(
            toolbar,
            textvariable=self.filter_var,
            values=[
                "All",
                "Query",
                "Chart"
            ],
            state="readonly",
            width=12,
            font=("Segoe UI", 9)
        )

        self.filter_combo.pack(
            side="left",
            padx=5,
            pady=8
        )


        self.filter_combo.bind(
            "<<ComboboxSelected>>",
            lambda event: self.search_history()
        )


        # ----------------------------------------------------
        # REFRESH
        # ----------------------------------------------------

        tk.Button(
            toolbar,
            text="↻ Refresh",
            font=("Segoe UI", 9, "bold"),
            bg=ACCENT_COLOR,
            fg=TEXT_COLOR,
            activebackground=HOVER_COLOR,
            activeforeground=TEXT_COLOR,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.load_history
        ).pack(
            side="left",
            padx=8,
            ipadx=10,
            ipady=5
        )


        # ----------------------------------------------------
        # CLEAR HISTORY
        # ----------------------------------------------------

        tk.Button(
            toolbar,
            text="🗑 Clear History",
            font=("Segoe UI", 9, "bold"),
            bg=DANGER_COLOR,
            fg=TEXT_COLOR,
            activebackground="#FF7885",
            activeforeground=TEXT_COLOR,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.clear_history
        ).pack(
            side="right",
            padx=15,
            ipadx=10,
            ipady=5
        )


        # ====================================================
        # HISTORY CARD
        # ====================================================

        history_card = tk.Frame(
            main,
            bg=CARD_COLOR
        )

        history_card.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )


        # ====================================================
        # TREEVIEW FRAME
        # ====================================================

        tree_frame = tk.Frame(
            history_card,
            bg=CARD_COLOR
        )

        tree_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )


        # ====================================================
        # VERTICAL SCROLLBAR
        # ====================================================

        vertical_scroll = ttk.Scrollbar(
            tree_frame,
            orient="vertical"
        )

        vertical_scroll.pack(
            side="right",
            fill="y"
        )


        # ====================================================
        # HORIZONTAL SCROLLBAR
        # ====================================================

        horizontal_scroll = ttk.Scrollbar(
            tree_frame,
            orient="horizontal"
        )

        horizontal_scroll.pack(
            side="bottom",
            fill="x"
        )


        # ====================================================
        # TREEVIEW
        # ====================================================

        columns = (
            "id",
            "date_time",
            "database",
            "question",
            "sql",
            "rows",
            "type",
            "chart"
        )


        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set
        )


        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )


        vertical_scroll.config(
            command=self.tree.yview
        )


        horizontal_scroll.config(
            command=self.tree.xview
        )


        # ====================================================
        # HEADINGS
        # ====================================================

        headings = {
            "id": "ID",
            "date_time": "Date / Time",
            "database": "Database",
            "question": "Question",
            "sql": "SQL Query",
            "rows": "Rows",
            "type": "Type",
            "chart": "Chart"
        }


        widths = {
            "id": 60,
            "date_time": 150,
            "database": 150,
            "question": 300,
            "sql": 450,
            "rows": 80,
            "type": 100,
            "chart": 120
        }


        for column in columns:

            self.tree.heading(
                column,
                text=headings[column]
            )


            self.tree.column(
                column,
                width=widths[column],
                minwidth=60,
                anchor="w"
            )


        # ====================================================
        # DOUBLE CLICK
        # ====================================================

        self.tree.bind(
            "<Double-1>",
            self.show_selected_history
        )


        # ====================================================
        # STATUS
        # ====================================================

        self.status_label = tk.Label(
            history_card,
            text="0 records",
            font=("Segoe UI", 9),
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT
        )

        self.status_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 12)
        )


    # ========================================================
    # LOAD HISTORY
    # ========================================================

    def load_history(self):

        try:

            connection = sqlite3.connect(
                HISTORY_DB
            )

            cursor = connection.cursor()


            cursor.execute(
                """
                SELECT
                    id,
                    date_time,
                    database_name,
                    question,
                    sql_query,
                    rows_returned,
                    action_type,
                    chart_type
                FROM history
                ORDER BY id DESC
                """
            )


            self.history_data = cursor.fetchall()

            connection.close()


            self.display_history(
                self.history_data
            )


        except Exception as error:

            messagebox.showerror(
                "History Error",
                str(error)
            )


    # ========================================================
    # DISPLAY HISTORY
    # ========================================================

    def display_history(
        self,
        data
    ):

        for item in self.tree.get_children():

            self.tree.delete(
                item
            )


        for record in data:

            self.tree.insert(
                "",
                "end",
                values=record
            )


        self.status_label.config(
            text=f"{len(data)} record(s)"
        )


    # ========================================================
    # SEARCH HISTORY
    # ========================================================

    def search_history(self):

        search_text = (
            self.search_var
            .get()
            .strip()
            .lower()
        )


        selected_filter = (
            self.filter_var
            .get()
        )


        filtered = []


        for record in self.history_data:

            # ----------------------------------------------
            # TYPE FILTER
            # ----------------------------------------------

            action_type = str(
                record[6]
            ).lower()


            if selected_filter == "Query":

                if action_type != "query":

                    continue


            elif selected_filter == "Chart":

                if action_type != "chart":

                    continue


            # ----------------------------------------------
            # SEARCH
            # ----------------------------------------------

            if search_text:

                searchable = " ".join(
                    str(value)
                    for value in record
                ).lower()


                if search_text not in searchable:

                    continue


            filtered.append(
                record
            )


        self.display_history(
            filtered
        )


    # ========================================================
    # ADD QUERY HISTORY
    # ========================================================

    def add_history(
        self,
        database_name,
        question,
        sql_query,
        rows_returned=0
    ):

        try:

            from datetime import datetime


            date_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )


            connection = sqlite3.connect(
                HISTORY_DB
            )

            cursor = connection.cursor()


            cursor.execute(
                """
                INSERT INTO history
                (
                    date_time,
                    database_name,
                    question,
                    sql_query,
                    rows_returned,
                    action_type,
                    chart_type
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    date_time,
                    database_name,
                    question,
                    sql_query,
                    rows_returned,
                    "QUERY",
                    ""
                )
            )


            connection.commit()

            connection.close()


            self.load_history()


        except Exception as error:

            print(
                "Could not save query history:",
                error
            )


    # ========================================================
    # ADD CHART HISTORY
    # ========================================================

    def add_chart_history(
        self,
        database_name,
        question,
        sql_query,
        chart_type,
        rows_returned=0
    ):

        try:

            from datetime import datetime


            date_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )


            connection = sqlite3.connect(
                HISTORY_DB
            )

            cursor = connection.cursor()


            cursor.execute(
                """
                INSERT INTO history
                (
                    date_time,
                    database_name,
                    question,
                    sql_query,
                    rows_returned,
                    action_type,
                    chart_type
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    date_time,
                    database_name,
                    question,
                    sql_query,
                    rows_returned,
                    "CHART",
                    chart_type
                )
            )


            connection.commit()

            connection.close()


            self.load_history()


        except Exception as error:

            print(
                "Could not save chart history:",
                error
            )


    # ========================================================
    # SHOW SELECTED HISTORY
    # ========================================================

    def show_selected_history(
        self,
        event=None
    ):

        selected = self.tree.selection()


        if not selected:

            return


        item = self.tree.item(
            selected[0]
        )


        values = item.get(
            "values",
            []
        )


        if not values:

            return


        record_window = tk.Toplevel(
            self.parent.winfo_toplevel()
        )

        record_window.title(
            "History Details"
        )

        record_window.geometry(
            "850x650"
        )

        record_window.minsize(
            700,
            500
        )

        record_window.configure(
            bg=BG_COLOR
        )


        # ====================================================
        # TITLE
        # ====================================================

        tk.Label(
            record_window,
            text="History Details",
            font=("Segoe UI", 20, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 15)
        )


        # ====================================================
        # INFORMATION
        # ====================================================

        info = tk.Frame(
            record_window,
            bg=CARD_COLOR
        )

        info.pack(
            fill="x",
            padx=25,
            pady=5
        )


        labels = [
            ("ID", values[0]),
            ("Date / Time", values[1]),
            ("Database", values[2]),
            ("Rows", values[5]),
            ("Type", values[6]),
            ("Chart", values[7])
        ]


        for index, (name, value) in enumerate(labels):

            tk.Label(
                info,
                text=name,
                font=("Segoe UI", 9, "bold"),
                bg=CARD_COLOR,
                fg=ACCENT_COLOR
            ).grid(
                row=index // 3,
                column=(index % 3) * 2,
                padx=(15, 5),
                pady=10,
                sticky="w"
            )


            tk.Label(
                info,
                text=str(value),
                font=("Segoe UI", 9),
                bg=CARD_COLOR,
                fg=TEXT_COLOR
            ).grid(
                row=index // 3,
                column=(index % 3) * 2 + 1,
                padx=(0, 20),
                pady=10,
                sticky="w"
            )


        # ====================================================
        # QUESTION
        # ====================================================

        question_card = tk.Frame(
            record_window,
            bg=CARD_COLOR
        )

        question_card.pack(
            fill="x",
            padx=25,
            pady=10
        )


        tk.Label(
            question_card,
            text="Question",
            font=("Segoe UI", 10, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 5)
        )


        tk.Label(
            question_card,
            text=str(values[3]),
            font=("Segoe UI", 10),
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT,
            wraplength=760,
            justify="left"
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )


        # ====================================================
        # SQL
        # ====================================================

        sql_card = tk.Frame(
            record_window,
            bg=CARD_COLOR
        )

        sql_card.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )


        tk.Label(
            sql_card,
            text="SQL Query",
            font=("Segoe UI", 10, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 5)
        )


        sql_frame = tk.Frame(
            sql_card,
            bg=INPUT_COLOR
        )

        sql_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )


        sql_scroll = tk.Scrollbar(
            sql_frame,
            orient="vertical"
        )

        sql_scroll.pack(
            side="right",
            fill="y"
        )


        sql_text = tk.Text(
            sql_frame,
            font=("Consolas", 10),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            relief="flat",
            bd=0,
            wrap="word",
            yscrollcommand=sql_scroll.set
        )

        sql_text.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )


        sql_scroll.config(
            command=sql_text.yview
        )


        sql_text.insert(
            "1.0",
            str(values[4])
        )


        sql_text.config(
            state="disabled"
        )


    # ========================================================
    # CLEAR HISTORY
    # ========================================================

    def clear_history(self):

        confirm = messagebox.askyesno(
            "Clear History",
            (
                "Are you sure you want to delete "
                "ALL SQL and chart history?"
            )
        )


        if not confirm:

            return


        try:

            connection = sqlite3.connect(
                HISTORY_DB
            )

            cursor = connection.cursor()


            cursor.execute(
                "DELETE FROM history"
            )


            connection.commit()


            # Reset AUTOINCREMENT

            cursor.execute(
                """
                DELETE FROM sqlite_sequence
                WHERE name='history'
                """
            )


            connection.commit()

            connection.close()


            self.history_data = []


            self.display_history(
                []
            )


            messagebox.showinfo(
                "History Cleared",
                "All history has been deleted."
            )


        except Exception as error:

            messagebox.showerror(
                "Clear History Error",
                str(error)
            )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.title(
        "AI SQL Studio - SQL History"
    )

    root.geometry(
        "1250x750"
    )

    root.minsize(
        1000,
        650
    )

    root.configure(
        bg=BG_COLOR
    )


    SQLHistory(
        root
    )


    root.mainloop()