# ============================================================
# QUERY_BUILDER.PY
# AI SQL GENERATOR + PERSISTENT HISTORY
#
# Supports:
# SQLite  -> .db .sqlite .sqlite3
# CSV     -> .csv
# Excel   -> .xlsx .xls
# JSON    -> .json
# TSV     -> .tsv
# TXT     -> .txt
#
# Features:
# - Natural language -> SQL using Ollama
# - Execute read-only SQL
# - Display query results
# - Visualize query results
# - Save executed SQL queries
# - Save generated charts
# - Persistent history using sql_history.json
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import sqlite3
import json
import urllib.request
import urllib.error
import re
import os
from datetime import datetime


# ============================================================
# OPTIONAL PANDAS
# ============================================================

try:
    import pandas as pd
except ImportError:
    pd = None


# ============================================================
# MATPLOTLIB
# ============================================================

try:

    import matplotlib

    matplotlib.use("TkAgg")

    from matplotlib.figure import Figure

    from matplotlib.backends.backend_tkagg import (
        FigureCanvasTkAgg
    )

except ImportError:

    Figure = None
    FigureCanvasTkAgg = None


# ============================================================
# COLORS
# ============================================================

BG_COLOR = "#101522"
CARD_COLOR = "#1C2433"
INPUT_COLOR = "#252D3D"

ACCENT_COLOR = "#6C63E8"
ACCENT_HOVER = "#7A72F5"

TEXT_COLOR = "#FFFFFF"
SECONDARY_TEXT = "#AAB2C0"

SUCCESS_COLOR = "#35D07F"
DANGER_COLOR = "#FF5C6C"
WARNING_COLOR = "#FFD166"


# ============================================================
# OLLAMA SETTINGS
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"

OLLAMA_MODEL = "llama3.2"


# ============================================================
# HISTORY FILE
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

HISTORY_FILE = os.path.join(
    BASE_DIR,
    "sql_history.json"
)


# ============================================================
# QUERY BUILDER
# ============================================================

class QueryBuilder:

    def __init__(
        self,
        parent,
        db_path=None,
        current_table=None,
        back_command=None
    ):

        self.parent = parent

        self.db_path = db_path

        self.current_table = current_table

        self.back_command = back_command

        self.connection = None

        self.tables = []

        self.columns = []

        self.last_sql = ""

        self.last_question = ""

        self.last_result = []

        self.last_column_names = []

        self.source_file_type = ""

        # History
        self.history_file = HISTORY_FILE

        self.create_history_file()

        self.create_ui()

        # ----------------------------------------------------
        # Existing database/file
        # ----------------------------------------------------

        if self.db_path:

            self.connect_existing_database()


    # ========================================================
    # HISTORY STORAGE
    # ========================================================

    def create_history_file(self):

        try:

            if not os.path.exists(
                self.history_file
            ):

                with open(
                    self.history_file,
                    "w",
                    encoding="utf-8"
                ) as file:

                    json.dump(
                        [],
                        file,
                        indent=4
                    )

        except Exception as error:

            print(
                "History file creation error:",
                error
            )


    # ========================================================
    # LOAD HISTORY
    # ========================================================

    def load_history_data(self):

        try:

            if not os.path.exists(
                self.history_file
            ):

                return []

            with open(
                self.history_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if isinstance(
                data,
                list
            ):

                return data

            return []

        except Exception as error:

            print(
                "History loading error:",
                error
            )

            return []


    # ========================================================
    # SAVE HISTORY DATA
    # ========================================================

    def save_history_data(
        self,
        history_data
    ):

        try:

            with open(
                self.history_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    history_data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

        except Exception as error:

            print(
                "History saving error:",
                error
            )


    # ========================================================
    # ADD QUERY HISTORY
    # ========================================================

    def save_query_history(
        self,
        question,
        sql,
        database_name,
        row_count
    ):

        try:

            history_data = (
                self.load_history_data()
            )

            new_id = 1

            if history_data:

                ids = []

                for item in history_data:

                    try:

                        ids.append(
                            int(
                                item.get(
                                    "id",
                                    0
                                )
                            )
                        )

                    except Exception:

                        pass

                if ids:

                    new_id = max(ids) + 1


            now = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )


            item = {

                "id": new_id,

                "date": now,

                "database": database_name,

                "query": sql,

                "type": "query",

                "question": question,

                "sql": sql,

                "rows": row_count,

                "chart_type": "",

                "x_column": "",

                "y_column": ""

            }


            history_data.append(
                item
            )


            self.save_history_data(
                history_data
            )


            print(
                "SQL history saved."
            )


        except Exception as error:

            print(
                "Could not save query history:",
                error
            )


    # ========================================================
    # ADD CHART HISTORY
    # ========================================================

    def save_chart_history(
        self,
        chart_type,
        x_column,
        y_column
    ):

        try:

            history_data = (
                self.load_history_data()
            )

            new_id = 1

            if history_data:

                ids = []

                for item in history_data:

                    try:

                        ids.append(
                            int(
                                item.get(
                                    "id",
                                    0
                                )
                            )
                        )

                    except Exception:

                        pass

                if ids:

                    new_id = max(ids) + 1


            now = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )


            database_name = (
                os.path.basename(
                    self.db_path
                )
                if self.db_path
                else "Unknown"
            )


            chart_query = (
                f"[CHART] "
                f"{chart_type} | "
                f"X: {x_column} | "
                f"Y: {y_column}"
            )


            item = {

                "id": new_id,

                "date": now,

                "database": database_name,

                "query": chart_query,

                "type": "chart",

                "question": self.last_question,

                "sql": self.last_sql,

                "rows": len(
                    self.last_result
                ),

                "chart_type": chart_type,

                "x_column": x_column,

                "y_column": y_column

            }


            history_data.append(
                item
            )


            self.save_history_data(
                history_data
            )


            print(
                "Chart history saved."
            )


        except Exception as error:

            print(
                "Could not save chart history:",
                error
            )


    # ========================================================
    # DATABASE NAME
    # ========================================================

    def get_database_name(self):

        if not self.db_path:

            return "Unknown"

        try:

            return os.path.basename(
                self.db_path
            )

        except Exception:

            return str(
                self.db_path
            )


    # ========================================================
    # CREATE UI
    # ========================================================

    def create_ui(self):

        for widget in self.parent.winfo_children():

            widget.destroy()


        # ====================================================
        # MAIN
        # ====================================================

        self.main = tk.Frame(
            self.parent,
            bg=BG_COLOR
        )

        self.main.pack(
            fill="both",
            expand=True
        )


        # ====================================================
        # HEADER
        # ====================================================

        header = tk.Frame(
            self.main,
            bg=BG_COLOR
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(22, 10)
        )


        tk.Label(
            header,
            text="⚡ AI SQL Generator",
            font=("Segoe UI", 25, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w"
        )


        tk.Label(
            header,
            text=(
                "Ask questions in normal English. "
                "Ollama converts them into SQL and retrieves the answer."
            ),
            font=("Segoe UI", 10),
            bg=BG_COLOR,
            fg=SECONDARY_TEXT
        ).pack(
            anchor="w",
            pady=(4, 0)
        )


        # ====================================================
        # FILE BAR
        # ====================================================

        database_bar = tk.Frame(
            self.main,
            bg=CARD_COLOR
        )

        database_bar.pack(
            fill="x",
            padx=30,
            pady=8
        )


        tk.Label(
            database_bar,
            text="DATA SOURCE",
            font=("Segoe UI", 8, "bold"),
            bg=CARD_COLOR,
            fg=ACCENT_COLOR
        ).grid(
            row=0,
            column=0,
            padx=(18, 8),
            pady=(10, 2),
            sticky="w"
        )


        self.database_label = tk.Label(
            database_bar,
            text="No file selected",
            font=("Segoe UI", 10, "bold"),
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT
        )

        self.database_label.grid(
            row=1,
            column=0,
            padx=(18, 8),
            pady=(0, 12),
            sticky="w"
        )


        tk.Label(
            database_bar,
            text="TABLE",
            font=("Segoe UI", 8, "bold"),
            bg=CARD_COLOR,
            fg=ACCENT_COLOR
        ).grid(
            row=0,
            column=1,
            padx=15,
            pady=(10, 2),
            sticky="w"
        )


        self.table_combo = ttk.Combobox(
            database_bar,
            state="readonly",
            width=25,
            font=("Segoe UI", 10)
        )

        self.table_combo.grid(
            row=1,
            column=1,
            padx=15,
            pady=(0, 12)
        )


        self.table_combo.bind(
            "<<ComboboxSelected>>",
            self.table_changed
        )


        tk.Button(
            database_bar,
            text="📂 Select Data File",
            font=("Segoe UI", 9, "bold"),
            bg=ACCENT_COLOR,
            fg=TEXT_COLOR,
            activebackground=ACCENT_HOVER,
            activeforeground=TEXT_COLOR,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.select_database
        ).grid(
            row=0,
            column=2,
            rowspan=2,
            padx=15,
            pady=10,
            ipadx=10,
            ipady=5
        )


        # ====================================================
        # QUESTION CARD
        # ====================================================

        question_card = tk.Frame(
            self.main,
            bg=CARD_COLOR
        )

        question_card.pack(
            fill="x",
            padx=30,
            pady=8
        )


        tk.Label(
            question_card,
            text="ASK YOUR QUESTION",
            font=("Segoe UI", 9, "bold"),
            bg=CARD_COLOR,
            fg=ACCENT_COLOR
        ).pack(
            anchor="w",
            padx=18,
            pady=(14, 5)
        )


        question_frame = tk.Frame(
            question_card,
            bg=INPUT_COLOR
        )

        question_frame.pack(
            fill="x",
            padx=18,
            pady=(0, 12)
        )


        self.question_text = tk.Text(
            question_frame,
            height=4,
            font=("Segoe UI", 11),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            relief="flat",
            bd=0,
            wrap="word"
        )

        self.question_text.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=8
        )


        self.question_text.insert(
            "1.0",
            "Example: Show the top 5 records."
        )


        # ====================================================
        # BUTTONS
        # ====================================================

        button_frame = tk.Frame(
            question_card,
            bg=CARD_COLOR
        )

        button_frame.pack(
            fill="x",
            padx=18,
            pady=(0, 15)
        )


        self.generate_button = tk.Button(
            button_frame,
            text="✨ Generate SQL & Get Answer",
            font=("Segoe UI", 10, "bold"),
            bg=ACCENT_COLOR,
            fg=TEXT_COLOR,
            activebackground=ACCENT_HOVER,
            activeforeground=TEXT_COLOR,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.generate_sql
        )

        self.generate_button.pack(
            side="left",
            ipadx=15,
            ipady=7
        )


        tk.Button(
            button_frame,
            text="Clear",
            font=("Segoe UI", 9, "bold"),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            activebackground="#303A4E",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.clear_all
        ).pack(
            side="left",
            padx=10,
            ipadx=12,
            ipady=7
        )


        self.status_label = tk.Label(
            button_frame,
            text="Ollama: Ready",
            font=("Segoe UI", 9),
            bg=CARD_COLOR,
            fg=SUCCESS_COLOR
        )

        self.status_label.pack(
            side="right"
        )


        # ====================================================
        # CONTENT AREA
        # ====================================================

        content_frame = tk.Frame(
            self.main,
            bg=BG_COLOR
        )

        content_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 20)
        )


        # ====================================================
        # SQL CARD
        # ====================================================

        sql_card = tk.Frame(
            content_frame,
            bg=CARD_COLOR
        )

        sql_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 7)
        )


        tk.Label(
            sql_card,
            text="Generated SQL",
            font=("Segoe UI", 13, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 8)
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


        self.sql_text = tk.Text(
            sql_frame,
            font=("Consolas", 10),
            bg=INPUT_COLOR,
            fg="#D9DDF0",
            insertbackground=TEXT_COLOR,
            relief="flat",
            bd=0,
            wrap="word",
            yscrollcommand=sql_scroll.set
        )

        self.sql_text.pack(
            side="left",
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )


        sql_scroll.config(
            command=self.sql_text.yview
        )


        # ====================================================
        # ANSWER CARD
        # ====================================================

        answer_card = tk.Frame(
            content_frame,
            bg=CARD_COLOR
        )

        answer_card.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(7, 0)
        )


        tk.Label(
            answer_card,
            text="🤖 AI Answer",
            font=("Segoe UI", 13, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 8)
        )


        answer_frame = tk.Frame(
            answer_card,
            bg=INPUT_COLOR
        )

        answer_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )


        answer_scroll = tk.Scrollbar(
            answer_frame,
            orient="vertical"
        )

        answer_scroll.pack(
            side="right",
            fill="y"
        )


        self.answer_text = tk.Text(
            answer_frame,
            font=("Segoe UI", 10),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            relief="flat",
            bd=0,
            wrap="word",
            yscrollcommand=answer_scroll.set
        )

        self.answer_text.pack(
            side="left",
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )


        answer_scroll.config(
            command=self.answer_text.yview
        )


        # ====================================================
        # RESULT
        # ====================================================

        result_outer = tk.Frame(
            self.main,
            bg=CARD_COLOR
        )

        result_outer.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 20)
        )


        result_header = tk.Frame(
            result_outer,
            bg=CARD_COLOR
        )

        result_header.pack(
            fill="x",
            padx=15,
            pady=(15, 8)
        )


        tk.Label(
            result_header,
            text="📊 Query Result",
            font=("Segoe UI", 13, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            side="left"
        )


        self.visualize_button = tk.Button(
            result_header,
            text="📈 Visualize Result",
            font=("Segoe UI", 9, "bold"),
            bg=ACCENT_COLOR,
            fg=TEXT_COLOR,
            activebackground=ACCENT_HOVER,
            activeforeground=TEXT_COLOR,
            relief="flat",
            bd=0,
            cursor="hand2",
            state="disabled",
            command=self.visualize_result
        )

        self.visualize_button.pack(
            side="right",
            ipadx=10,
            ipady=5
        )


        self.result_frame = tk.Frame(
            result_outer,
            bg=CARD_COLOR
        )

        self.result_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )


        self.create_empty_result()


        if self.db_path:

            self.database_label.config(
                text=os.path.basename(
                    self.db_path
                ),
                fg=SUCCESS_COLOR
            )


        self.question_text.focus_set()


    # ========================================================
    # CONNECT FILE
    # ========================================================

    def connect_existing_database(self):

        if not self.db_path:

            return

        try:

            self.load_data_file(
                self.db_path
            )

        except Exception as error:

            messagebox.showerror(
                "Data Error",
                str(error)
            )


    # ========================================================
    # SELECT DATA FILE
    # ========================================================

    def select_database(self):

        path = filedialog.askopenfilename(

            title="Select Data File",

            filetypes=[

                (
                    "Supported Data Files",
                    "*.db *.sqlite *.sqlite3 "
                    "*.csv *.xlsx *.xls *.json *.tsv *.txt"
                ),

                (
                    "SQLite Database",
                    "*.db *.sqlite *.sqlite3"
                ),

                (
                    "CSV Files",
                    "*.csv"
                ),

                (
                    "Excel Files",
                    "*.xlsx *.xls"
                ),

                (
                    "JSON Files",
                    "*.json"
                ),

                (
                    "TSV Files",
                    "*.tsv"
                ),

                (
                    "Text Files",
                    "*.txt"
                ),

                (
                    "All Files",
                    "*.*"
                )

            ]
        )


        if not path:

            return


        try:

            self.load_data_file(
                path
            )

            messagebox.showinfo(
                "Data Loaded",
                "Data loaded successfully."
            )

        except Exception as error:

            self.connection = None

            messagebox.showerror(
                "Data Error",
                str(error)
            )


    # ========================================================
    # LOAD DATA FILE
    # ========================================================

    def load_data_file(
        self,
        path
    ):

        extension = (
            os.path.splitext(path)[1]
            .lower()
        )

        self.db_path = path

        self.current_table = None

        self.source_file_type = extension


        # ----------------------------------------------------
        # Close old connection
        # ----------------------------------------------------

        if self.connection:

            try:

                self.connection.close()

            except:

                pass


        # ----------------------------------------------------
        # SQLITE DATABASE
        # ----------------------------------------------------

        if extension in (
            ".db",
            ".sqlite",
            ".sqlite3"
        ):

            self.connection = sqlite3.connect(
                path
            )

            self.database_label.config(
                text=os.path.basename(path),
                fg=SUCCESS_COLOR
            )

            self.load_tables()

            return


        # ----------------------------------------------------
        # OTHER FILES
        # ----------------------------------------------------

        if pd is None:

            raise Exception(
                "Pandas is required for CSV, Excel, JSON, TSV "
                "and TXT files.\n\n"
                "Install it using:\n"
                "pip install pandas openpyxl"
            )


        dataframe = self.read_dataframe(
            path,
            extension
        )


        if dataframe is None:

            raise Exception(
                "Could not read the selected file."
            )


        if dataframe.empty:

            raise Exception(
                "The selected file contains no data."
            )


        # ----------------------------------------------------
        # Temporary SQLite database
        # ----------------------------------------------------

        self.connection = sqlite3.connect(
            ":memory:"
        )


        table_name = self.create_safe_table_name(
            os.path.splitext(
                os.path.basename(path)
            )[0]
        )


        dataframe.columns = self.make_unique_columns(
            dataframe.columns
        )


        dataframe.to_sql(
            table_name,
            self.connection,
            index=False,
            if_exists="replace"
        )


        self.current_table = table_name


        self.database_label.config(
            text=(
                os.path.basename(path)
                + "  ["
                + extension.upper()
                + "]"
            ),
            fg=SUCCESS_COLOR
        )


        self.load_tables()


        if table_name in self.tables:

            self.table_combo.set(
                table_name
            )

            self.current_table = table_name

            self.load_columns()


    # ========================================================
    # READ DATAFRAME
    # ========================================================

    def read_dataframe(
        self,
        path,
        extension
    ):

        if extension == ".csv":

            return pd.read_csv(
                path
            )


        if extension == ".tsv":

            return pd.read_csv(
                path,
                sep="\t"
            )


        if extension in (
            ".xlsx",
            ".xls"
        ):

            return pd.read_excel(
                path
            )


        if extension == ".json":

            try:

                return pd.read_json(
                    path
                )

            except ValueError:

                with open(
                    path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    data = json.load(file)


                if isinstance(
                    data,
                    list
                ):

                    return pd.DataFrame(
                        data
                    )


                if isinstance(
                    data,
                    dict
                ):

                    return pd.DataFrame(
                        data
                    )


        if extension == ".txt":

            try:

                return pd.read_csv(
                    path
                )

            except Exception:

                return pd.read_csv(
                    path,
                    sep=None,
                    engine="python"
                )


        raise Exception(
            f"Unsupported file type: {extension}"
        )


    # ========================================================
    # SAFE TABLE NAME
    # ========================================================

    def create_safe_table_name(
        self,
        name
    ):

        name = re.sub(
            r"[^a-zA-Z0-9_]+",
            "_",
            name
        )


        if not name:

            name = "data"


        if name[0].isdigit():

            name = "table_" + name


        return name.lower()


    # ========================================================
    # UNIQUE COLUMNS
    # ========================================================

    def make_unique_columns(
        self,
        columns
    ):

        result = []

        used = {}


        for column in columns:

            name = str(
                column
            ).strip()


            name = re.sub(
                r"\s+",
                "_",
                name
            )


            name = re.sub(
                r"[^a-zA-Z0-9_]",
                "_",
                name
            )


            if not name:

                name = "column"


            if name[0].isdigit():

                name = "column_" + name


            original = name

            counter = 1


            while name.lower() in used:

                counter += 1

                name = (
                    original
                    + "_"
                    + str(counter)
                )


            used[
                name.lower()
            ] = True


            result.append(
                name
            )


        return result


    # ========================================================
    # LOAD TABLES
    # ========================================================

    def load_tables(self):

        if not self.connection:

            return


        try:

            cursor = self.connection.cursor()


            cursor.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                AND name NOT LIKE 'sqlite_%'
                ORDER BY name
                """
            )


            rows = cursor.fetchall()


            self.tables = [
                row[0]
                for row in rows
            ]


            self.table_combo["values"] = (
                self.tables
            )


            if self.tables:

                if (
                    self.current_table
                    and
                    self.current_table in self.tables
                ):

                    self.table_combo.set(
                        self.current_table
                    )

                else:

                    self.table_combo.current(
                        0
                    )

                    self.current_table = (
                        self.tables[0]
                    )


                self.load_columns()


            else:

                self.table_combo.set("")

                self.columns = []


        except Exception as error:

            messagebox.showerror(
                "Table Error",
                str(error)
            )


    # ========================================================
    # TABLE CHANGED
    # ========================================================

    def table_changed(
        self,
        event=None
    ):

        table = (
            self.table_combo
            .get()
            .strip()
        )


        if not table:

            return


        self.current_table = table

        self.load_columns()


    # ========================================================
    # LOAD COLUMNS
    # ========================================================

    def load_columns(self):

        if not self.connection:

            return


        if not self.current_table:

            return


        try:

            cursor = self.connection.cursor()


            cursor.execute(
                f'PRAGMA table_info("{self.current_table}")'
            )


            rows = cursor.fetchall()


            self.columns = [
                row[1]
                for row in rows
            ]


        except Exception:

            self.columns = []


    # ========================================================
    # EMPTY RESULT
    # ========================================================

    def create_empty_result(self):

        if hasattr(
            self,
            "visualize_button"
        ):

            self.visualize_button.config(
                state="disabled"
            )


        for widget in (
            self.result_frame
            .winfo_children()
        ):

            widget.destroy()


        tk.Label(
            self.result_frame,
            text="Ask a question to see database results.",
            font=("Segoe UI", 10),
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT
        ).pack(
            pady=30
        )


    # ========================================================
    # GENERATE SQL
    # ========================================================

    def generate_sql(self):

        question = (
            self.question_text
            .get(
                "1.0",
                tk.END
            )
            .strip()
        )


        if not question:

            messagebox.showwarning(
                "Question Required",
                "Please ask a question first."
            )

            return


        if question.lower() == (
            "example: show the top 5 records."
        ):

            messagebox.showwarning(
                "Question Required",
                "Replace the example with your own question."
            )

            return


        if not self.connection:

            messagebox.showwarning(
                "Data Required",
                "Please select a data file first."
            )

            return


        if not self.current_table:

            messagebox.showwarning(
                "Table Required",
                "Please select a table first."
            )

            return


        if not self.columns:

            self.load_columns()


        if not self.columns:

            messagebox.showerror(
                "Schema Error",
                "Could not read table columns."
            )

            return


        self.last_question = question


        self.generate_button.config(
            state="disabled"
        )


        self.status_label.config(
            text="Ollama: Thinking...",
            fg=WARNING_COLOR
        )


        self.sql_text.delete(
            "1.0",
            tk.END
        )


        self.answer_text.delete(
            "1.0",
            tk.END
        )


        self.create_empty_result()


        self.parent.after(
            50,
            lambda: self.process_question(
                question
            )
        )


    # ========================================================
    # PROCESS QUESTION
    # ========================================================

    def process_question(
        self,
        question
    ):

        try:

            schema = self.get_schema_text()


            sql = self.ask_ollama_for_sql(
                question,
                schema
            )


            if not sql:

                raise Exception(
                    "Ollama did not return an SQL query."
                )


            sql = self.clean_sql(
                sql
            )


            valid, error_message = (
                self.validate_sql(
                    sql
                )
            )


            if not valid:

                raise Exception(
                    error_message
                )


            self.last_sql = sql


            self.sql_text.insert(
                "1.0",
                sql
            )


            self.status_label.config(
                text="Executing SQL...",
                fg=WARNING_COLOR
            )


            self.parent.update_idletasks()


            columns, rows = (
                self.execute_sql(
                    sql
                )
            )


            self.last_column_names = columns

            self.last_result = rows


            self.display_result(
                columns,
                rows
            )


            # =================================================
            # SAVE EXECUTED QUERY TO HISTORY
            # =================================================

            self.save_query_history(
                question=question,
                sql=sql,
                database_name=self.get_database_name(),
                row_count=len(rows)
            )


            self.status_label.config(
                text="Ollama: Creating answer...",
                fg=WARNING_COLOR
            )


            self.parent.update_idletasks()


            answer = self.ask_ollama_for_answer(
                question,
                sql,
                columns,
                rows
            )


            self.answer_text.insert(
                "1.0",
                answer
            )


            self.status_label.config(
                text="✓ Complete",
                fg=SUCCESS_COLOR
            )


        except urllib.error.URLError:

            self.status_label.config(
                text="Ollama: Offline",
                fg=DANGER_COLOR
            )


            messagebox.showerror(
                "Ollama Not Found",
                (
                    "Ollama could not be reached.\n\n"
                    "Make sure Ollama is running.\n\n"
                    "Then install your model:\n\n"
                    "ollama pull llama3.2"
                )
            )


        except Exception as error:

            self.status_label.config(
                text="Error",
                fg=DANGER_COLOR
            )


            self.answer_text.insert(
                "1.0",
                "Error:\n\n"
                + str(error)
            )


        finally:

            self.generate_button.config(
                state="normal"
            )


    # ========================================================
    # SCHEMA
    # ========================================================

    def get_schema_text(self):

        cursor = self.connection.cursor()


        cursor.execute(
            f'PRAGMA table_info("{self.current_table}")'
        )


        columns = cursor.fetchall()


        schema_lines = []


        for column in columns:

            column_name = column[1]

            column_type = column[2]

            not_null = column[3]

            primary_key = column[5]


            schema_lines.append(
                f"- {column_name}"
                f" | type={column_type}"
                f" | not_null={not_null}"
                f" | primary_key={primary_key}"
            )


        return "\n".join(
            schema_lines
        )


    # ========================================================
    # OLLAMA SQL
    # ========================================================

    def ask_ollama_for_sql(
        self,
        question,
        schema
    ):

        prompt = f"""
You are an expert SQLite SQL generator.

TABLE:
{self.current_table}

SCHEMA:
{schema}

USER QUESTION:
{question}

RULES:

1. Generate ONE valid SQLite query.
2. Use only the table and columns provided.
3. Do not invent columns.
4. Do not invent tables.
5. Answer the user's question accurately.
6. Only SELECT or WITH queries are allowed.
7. Never generate INSERT.
8. Never generate UPDATE.
9. Never generate DELETE.
10. Never generate DROP.
11. Never generate ALTER.
12. Never generate CREATE.
13. Never generate PRAGMA.
14. Do not include markdown.
15. Do not include explanation.
16. Return ONLY SQL.

SQL:
"""


        return self.call_ollama(
            prompt
        )


    # ========================================================
    # OLLAMA ANSWER
    # ========================================================

    def ask_ollama_for_answer(
        self,
        question,
        sql,
        columns,
        rows
    ):

        limited_rows = rows[:100]


        result_text = ""


        if columns:

            result_text += (
                "Columns: "
                + ", ".join(columns)
                + "\n\n"
            )


        for row in limited_rows:

            result_text += (
                str(row)
                + "\n"
            )


        if not result_text:

            result_text = (
                "No rows were returned."
            )


        prompt = f"""
You are a database assistant.

USER QUESTION:
{question}

SQL:
{sql}

RESULT:
{result_text}

Answer the user's question using ONLY the result.

Rules:

1. Be direct.
2. Do not invent information.
3. If the result contains records, summarize them.
4. If the result contains COUNT, SUM, AVG, MAX or MIN, clearly state the value.
5. If there are no records, say no matching records were found.
6. Keep the answer short.
7. Do not generate SQL.
"""


        return self.call_ollama(
            prompt
        )


    # ========================================================
    # CALL OLLAMA
    # ========================================================

    def call_ollama(
        self,
        prompt
    ):

        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }


        data = json.dumps(
            payload
        ).encode(
            "utf-8"
        )


        request = urllib.request.Request(
            OLLAMA_URL,
            data=data,
            headers={
                "Content-Type":
                "application/json"
            },
            method="POST"
        )


        with urllib.request.urlopen(
            request,
            timeout=120
        ) as response:

            response_data = json.loads(
                response.read().decode(
                    "utf-8"
                )
            )


        return response_data.get(
            "response",
            ""
        ).strip()


    # ========================================================
    # CLEAN SQL
    # ========================================================

    def clean_sql(
        self,
        sql
    ):

        sql = sql.strip()


        sql = re.sub(
            r"^```sql\s*",
            "",
            sql,
            flags=re.IGNORECASE
        )


        sql = re.sub(
            r"^```\s*",
            "",
            sql
        )


        sql = re.sub(
            r"\s*```$",
            "",
            sql
        )


        sql = sql.strip()


        if sql.lower().startswith(
            "sql:"
        ):

            sql = sql[4:].strip()


        match = re.search(
            r"\b(SELECT|WITH)\b",
            sql,
            re.IGNORECASE
        )


        if match:

            sql = sql[
                match.start():
            ]


        if sql.endswith(";"):

            sql = sql[:-1]


        return sql.strip()


    # ========================================================
    # VALIDATE SQL
    # ========================================================

    def validate_sql(
        self,
        sql
    ):

        if not sql:

            return False, "Empty SQL query."


        normalized = (
            sql.strip()
            .lower()
        )


        if not (
            normalized.startswith("select")
            or
            normalized.startswith("with")
        ):

            return (
                False,
                "Only SELECT/WITH queries are allowed."
            )


        forbidden = [

            "insert ",

            "update ",

            "delete ",

            "drop ",

            "alter ",

            "create ",

            "replace ",

            "truncate ",

            "attach ",

            "detach ",

            "pragma ",

            "vacuum ",

            "reindex "

        ]


        for word in forbidden:

            if word in normalized:

                return (
                    False,
                    f"Unsafe SQL detected: {word.strip()}"
                )


        if ";" in sql:

            return (
                False,
                "Multiple SQL statements are not allowed."
            )


        return True, ""


    # ========================================================
    # EXECUTE SQL
    # ========================================================

    def execute_sql(
        self,
        sql
    ):

        cursor = self.connection.cursor()


        cursor.execute(
            sql
        )


        rows = cursor.fetchall()


        columns = []


        if cursor.description:

            columns = [

                description[0]

                for description
                in cursor.description

            ]


        return columns, rows


    # ========================================================
    # DISPLAY RESULT
    # ========================================================

    def display_result(
        self,
        columns,
        rows
    ):

        for widget in (
            self.result_frame
            .winfo_children()
        ):

            widget.destroy()


        if not columns:

            tk.Label(
                self.result_frame,
                text="Query executed successfully.",
                font=("Segoe UI", 10, "bold"),
                bg=CARD_COLOR,
                fg=SUCCESS_COLOR
            ).pack(
                pady=25
            )

            return


        tk.Label(
            self.result_frame,
            text=f"{len(rows)} row(s) returned",
            font=("Segoe UI", 9, "bold"),
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT
        ).pack(
            anchor="w",
            pady=(0, 5)
        )


        if self.last_result:

            self.visualize_button.config(
                state="normal"
            )


        table_frame = tk.Frame(
            self.result_frame,
            bg=CARD_COLOR
        )

        table_frame.pack(
            fill="both",
            expand=True
        )


        y_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical"
        )

        y_scroll.pack(
            side="right",
            fill="y"
        )


        x_scroll = ttk.Scrollbar(
            table_frame,
            orient="horizontal"
        )

        x_scroll.pack(
            side="bottom",
            fill="x"
        )


        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )


        tree.pack(
            side="left",
            fill="both",
            expand=True
        )


        y_scroll.config(
            command=tree.yview
        )


        x_scroll.config(
            command=tree.xview
        )


        for column in columns:

            tree.heading(
                column,
                text=column
            )


            tree.column(
                column,
                width=150,
                minwidth=80,
                anchor="w"
            )


        for row in rows:

            formatted = []


            for value in row:

                if value is None:

                    formatted.append(
                        "NULL"
                    )

                else:

                    formatted.append(
                        str(value)
                    )


            tree.insert(
                "",
                "end",
                values=formatted
            )


    # ========================================================
    # VISUALIZATION
    # ========================================================

    def visualize_result(self):

        if Figure is None:

            messagebox.showerror(
                "Visualization Not Available",
                "Install matplotlib using:\n\n"
                "pip install matplotlib"
            )

            return


        if not self.last_result:

            messagebox.showwarning(
                "No Result",
                "Execute a query first."
            )

            return


        chart_window = tk.Toplevel(
            self.parent.winfo_toplevel()
        )


        chart_window.title(
            "AI SQL Studio - Visualization"
        )


        chart_window.geometry(
            "1100x700"
        )


        chart_window.configure(
            bg=BG_COLOR
        )


        tk.Label(
            chart_window,
            text="📊 Query Visualization",
            font=("Segoe UI", 20, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w",
            padx=20,
            pady=15
        )


        controls = tk.Frame(
            chart_window,
            bg=CARD_COLOR
        )

        controls.pack(
            fill="x",
            padx=20,
            pady=8
        )


        tk.Label(
            controls,
            text="Chart Type",
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            side="left",
            padx=10
        )


        chart_type = tk.StringVar(
            value="Bar"
        )


        ttk.Combobox(
            controls,
            textvariable=chart_type,
            state="readonly",
            values=[
                "Bar",
                "Line",
                "Pie",
                "Scatter"
            ],
            width=12
        ).pack(
            side="left"
        )


        tk.Label(
            controls,
            text="X Column",
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            side="left",
            padx=(20, 8)
        )


        x_var = tk.StringVar()


        ttk.Combobox(
            controls,
            textvariable=x_var,
            state="readonly",
            values=self.last_column_names,
            width=20
        ).pack(
            side="left"
        )


        tk.Label(
            controls,
            text="Y Column",
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            side="left",
            padx=(20, 8)
        )


        y_var = tk.StringVar()


        ttk.Combobox(
            controls,
            textvariable=y_var,
            state="readonly",
            values=self.last_column_names,
            width=20
        ).pack(
            side="left"
        )


        chart_area = tk.Frame(
            chart_window,
            bg=CARD_COLOR
        )


        chart_area.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )


        if self.last_column_names:

            x_var.set(
                self.last_column_names[0]
            )


        if len(
            self.last_column_names
        ) > 1:

            y_var.set(
                self.last_column_names[1]
            )


        def is_number(value):

            try:

                float(value)

                return True

            except:

                return False


        def draw_chart():

            for widget in (
                chart_area
                .winfo_children()
            ):

                widget.destroy()


            x_column = x_var.get()

            y_column = y_var.get()

            selected = chart_type.get()


            if (
                x_column not in
                self.last_column_names
                or
                y_column not in
                self.last_column_names
            ):

                messagebox.showwarning(
                    "Invalid Columns",
                    "Select valid X and Y columns."
                )

                return


            indexes = {

                name: i

                for i, name

                in enumerate(
                    self.last_column_names
                )

            }


            xi = indexes[x_column]

            yi = indexes[y_column]


            x_values = []

            y_values = []


            for row in self.last_result[:1000]:

                xv = row[xi]

                yv = row[yi]


                if xv is None or yv is None:

                    continue


                if not is_number(yv):

                    continue


                x_values.append(
                    str(xv)
                )


                y_values.append(
                    float(yv)
                )


            if not x_values:

                messagebox.showwarning(
                    "No Data",
                    "Selected columns cannot be visualized."
                )

                return


            figure = Figure(
                figsize=(9, 5),
                dpi=100
            )


            axis = figure.add_subplot(
                111
            )


            figure.patch.set_facecolor(
                CARD_COLOR
            )


            axis.set_facecolor(
                INPUT_COLOR
            )


            if selected == "Bar":

                axis.bar(
                    x_values,
                    y_values
                )


            elif selected == "Line":

                axis.plot(
                    x_values,
                    y_values,
                    marker="o"
                )


            elif selected == "Pie":

                axis.pie(
                    y_values,
                    labels=x_values,
                    autopct="%1.1f%%"
                )


            elif selected == "Scatter":

                numeric_x = []

                numeric_y = []


                for row in self.last_result[:1000]:

                    xv = row[xi]

                    yv = row[yi]


                    if (
                        is_number(xv)
                        and
                        is_number(yv)
                    ):

                        numeric_x.append(
                            float(xv)
                        )

                        numeric_y.append(
                            float(yv)
                        )


                if not numeric_x:

                    messagebox.showwarning(
                        "Scatter Error",
                        "Scatter chart requires numeric X and Y columns."
                    )

                    return


                axis.scatter(
                    numeric_x,
                    numeric_y
                )


            axis.set_xlabel(
                x_column
            )


            axis.set_ylabel(
                y_column
            )


            axis.set_title(
                f"{y_column} by {x_column}"
            )


            axis.tick_params(
                axis="x",
                rotation=35
            )


            figure.tight_layout()


            canvas = FigureCanvasTkAgg(
                figure,
                master=chart_area
            )


            canvas.draw()


            canvas.get_tk_widget().pack(
                fill="both",
                expand=True,
                padx=10,
                pady=10
            )


            # =================================================
            # SAVE CHART HISTORY
            # =================================================

            self.save_chart_history(
                chart_type=selected,
                x_column=x_column,
                y_column=y_column
            )


        tk.Button(
            controls,
            text="Generate Chart",
            font=("Segoe UI", 9, "bold"),
            bg=ACCENT_COLOR,
            fg=TEXT_COLOR,
            activebackground=ACCENT_HOVER,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=draw_chart
        ).pack(
            side="right",
            padx=15,
            ipadx=10,
            ipady=5
        )


        draw_chart()


    # ========================================================
    # CLEAR
    # ========================================================

    def clear_all(self):

        self.question_text.delete(
            "1.0",
            tk.END
        )


        self.sql_text.delete(
            "1.0",
            tk.END
        )


        self.answer_text.delete(
            "1.0",
            tk.END
        )


        self.create_empty_result()


        self.last_result = []

        self.last_column_names = []

        self.last_sql = ""

        self.last_question = ""


        self.status_label.config(
            text="Ollama: Ready",
            fg=SUCCESS_COLOR
        )


        self.question_text.focus_set()


    # ========================================================
    # BACK
    # ========================================================

    def go_back(self):

        if self.back_command:

            try:

                self.back_command()

                return

            except Exception:

                pass


        messagebox.showinfo(
            "Navigation",
            "Use Dashboard navigation to change pages."
        )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()


    root.title(
        "AI SQL Studio - AI SQL Generator"
    )


    root.geometry(
        "1250x850"
    )


    root.minsize(
        1000,
        700
    )


    root.configure(
        bg=BG_COLOR
    )


    QueryBuilder(
        root
    )


    root.mainloop()