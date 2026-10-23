# ============================================================
# VISUALIZATION.PY
# AI SQL STUDIO - SMART DATA VISUALIZATION
# ============================================================

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
import os

# ============================================================
# PANDAS
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

    import matplotlib.pyplot as plt

    from matplotlib.backends.backend_tkagg import (
        FigureCanvasTkAgg
    )

except ImportError:
    plt = None
    FigureCanvasTkAgg = None


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
# VISUALIZATION CLASS
# ============================================================

class Visualization:

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

        self.dataframe = None

        self.figure = None
        self.canvas = None

        self.suggestion_data = {}

        self.create_ui()

        if self.db_path:

            self.load_database(
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
            pady=(22, 12)
        )


        tk.Label(
            header,
            text="📊 Data Visualization",
            font=("Segoe UI", 25, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w"
        )


        tk.Label(
            header,
            text="Upload your data and get intelligent chart recommendations",
            font=("Segoe UI", 10),
            bg=BG_COLOR,
            fg=SECONDARY_TEXT
        ).pack(
            anchor="w",
            pady=(4, 0)
        )


        # ====================================================
        # CONTENT
        # ====================================================

        content = tk.Frame(
            self.main,
            bg=BG_COLOR
        )

        content.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )


        # ====================================================
        # LEFT SCROLLABLE CONTROL PANEL
        # ====================================================

        left_container = tk.Frame(
            content,
            bg=CARD_COLOR,
            width=330
        )

        left_container.pack(
            side="left",
            fill="y",
            padx=(0, 10)
        )

        left_container.pack_propagate(False)


        self.control_canvas = tk.Canvas(
            left_container,
            bg=CARD_COLOR,
            highlightthickness=0,
            bd=0
        )

        self.control_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )


        control_scrollbar = ttk.Scrollbar(
            left_container,
            orient="vertical",
            command=self.control_canvas.yview
        )

        control_scrollbar.pack(
            side="right",
            fill="y"
        )


        self.control_canvas.configure(
            yscrollcommand=control_scrollbar.set
        )


        self.control_panel = tk.Frame(
            self.control_canvas,
            bg=CARD_COLOR
        )


        self.control_window = self.control_canvas.create_window(
            (0, 0),
            window=self.control_panel,
            anchor="nw"
        )


        self.control_panel.bind(
            "<Configure>",
            self.update_control_scroll
        )


        self.control_canvas.bind(
            "<Configure>",
            self.resize_control_panel
        )


        self.control_canvas.bind_all(
            "<MouseWheel>",
            self.mousewheel_scroll
        )


        # ====================================================
        # CONTROL TITLE
        # ====================================================

        tk.Label(
            self.control_panel,
            text="Chart Controls",
            font=("Segoe UI", 15, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        tk.Label(
            self.control_panel,
            text="Configure your visualization",
            font=("Segoe UI", 9),
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 18)
        )


        # ====================================================
        # DATA SOURCE
        # ====================================================

        tk.Label(
            self.control_panel,
            text="DATA SOURCE",
            font=("Segoe UI", 8, "bold"),
            bg=CARD_COLOR,
            fg=ACCENT_COLOR
        ).pack(
            anchor="w",
            padx=20,
            pady=(5, 5)
        )


        database_frame = tk.Frame(
            self.control_panel,
            bg=INPUT_COLOR
        )

        database_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )


        self.database_entry = tk.Entry(
            database_frame,
            font=("Segoe UI", 9),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            relief="flat",
            bd=0
        )

        self.database_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=8,
            pady=9
        )


        tk.Button(
            database_frame,
            text="...",
            font=("Segoe UI", 9, "bold"),
            bg=ACCENT_COLOR,
            fg=TEXT_COLOR,
            activebackground=HOVER_COLOR,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.select_database
        ).pack(
            side="right",
            padx=3,
            pady=3,
            ipadx=7,
            ipady=4
        )


        # ====================================================
        # TABLE
        # ====================================================

        tk.Label(
            self.control_panel,
            text="TABLE",
            font=("Segoe UI", 8, "bold"),
            bg=CARD_COLOR,
            fg=ACCENT_COLOR
        ).pack(
            anchor="w",
            padx=20,
            pady=(3, 5)
        )


        self.table_combo = ttk.Combobox(
            self.control_panel,
            state="readonly",
            font=("Segoe UI", 10)
        )

        self.table_combo.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )


        self.table_combo.bind(
            "<<ComboboxSelected>>",
            self.table_changed
        )


        # ====================================================
        # CHART TYPE
        # ====================================================

        tk.Label(
            self.control_panel,
            text="CHART TYPE",
            font=("Segoe UI", 8, "bold"),
            bg=CARD_COLOR,
            fg=ACCENT_COLOR
        ).pack(
            anchor="w",
            padx=20,
            pady=(3, 5)
        )


        self.chart_type = tk.StringVar(
            value="Bar"
        )


        self.chart_combo = ttk.Combobox(
            self.control_panel,
            textvariable=self.chart_type,
            state="readonly",
            values=[
                "Bar",
                "Line",
                "Pie",
                "Scatter",
                "Area",
                "Histogram"
            ],
            font=("Segoe UI", 10)
        )

        self.chart_combo.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )


        self.chart_combo.bind(
            "<<ComboboxSelected>>",
            self.chart_type_changed
        )


        # ====================================================
        # X AXIS
        # ====================================================

        tk.Label(
            self.control_panel,
            text="X-AXIS",
            font=("Segoe UI", 8, "bold"),
            bg=CARD_COLOR,
            fg=ACCENT_COLOR
        ).pack(
            anchor="w",
            padx=20,
            pady=(3, 5)
        )


        self.x_var = tk.StringVar()


        self.x_combo = ttk.Combobox(
            self.control_panel,
            textvariable=self.x_var,
            state="readonly",
            font=("Segoe UI", 10)
        )

        self.x_combo.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )


        # ====================================================
        # Y AXIS
        # ====================================================

        tk.Label(
            self.control_panel,
            text="Y-AXIS",
            font=("Segoe UI", 8, "bold"),
            bg=CARD_COLOR,
            fg=ACCENT_COLOR
        ).pack(
            anchor="w",
            padx=20,
            pady=(3, 5)
        )


        self.y_var = tk.StringVar()


        self.y_combo = ttk.Combobox(
            self.control_panel,
            textvariable=self.y_var,
            state="readonly",
            font=("Segoe UI", 10)
        )

        self.y_combo.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )


        # ====================================================
        # AGGREGATION
        # ====================================================

        tk.Label(
            self.control_panel,
            text="AGGREGATION",
            font=("Segoe UI", 8, "bold"),
            bg=CARD_COLOR,
            fg=ACCENT_COLOR
        ).pack(
            anchor="w",
            padx=20,
            pady=(3, 5)
        )


        self.aggregation_var = tk.StringVar(
            value="Sum"
        )


        self.aggregation_combo = ttk.Combobox(
            self.control_panel,
            textvariable=self.aggregation_var,
            state="readonly",
            values=[
                "Sum",
                "Average",
                "Count",
                "Minimum",
                "Maximum"
            ],
            font=("Segoe UI", 10)
        )

        self.aggregation_combo.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )


        # ====================================================
        # TOP N
        # ====================================================

        tk.Label(
            self.control_panel,
            text="DISPLAY",
            font=("Segoe UI", 8, "bold"),
            bg=CARD_COLOR,
            fg=ACCENT_COLOR
        ).pack(
            anchor="w",
            padx=20,
            pady=(3, 5)
        )


        self.top_n_var = tk.StringVar(
            value="All"
        )


        self.top_n_combo = ttk.Combobox(
            self.control_panel,
            textvariable=self.top_n_var,
            state="readonly",
            values=[
                "All",
                "Top 5",
                "Top 10",
                "Top 20"
            ],
            font=("Segoe UI", 10)
        )

        self.top_n_combo.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )


        # ====================================================
        # SMART SUGGESTION
        # ====================================================

        suggestion_box = tk.Frame(
            self.control_panel,
            bg=INPUT_COLOR
        )

        suggestion_box.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )


        tk.Label(
            suggestion_box,
            text="💡 SMART SUGGESTION",
            font=("Segoe UI", 8, "bold"),
            bg=INPUT_COLOR,
            fg=WARNING_COLOR
        ).pack(
            anchor="w",
            padx=12,
            pady=(10, 4)
        )


        self.suggestion_label = tk.Label(
            suggestion_box,
            text=(
                "Upload a file and click "
                "'Get Suggestion' to analyze it."
            ),
            font=("Segoe UI", 8),
            bg=INPUT_COLOR,
            fg=SECONDARY_TEXT,
            wraplength=270,
            justify="left"
        )

        self.suggestion_label.pack(
            fill="x",
            padx=12,
            pady=(0, 10)
        )


        # ====================================================
        # GET SUGGESTION BUTTON
        # ====================================================

        self.suggestion_button = tk.Button(
            self.control_panel,
            text="💡 Get Suggestion",
            font=("Segoe UI", 10, "bold"),
            bg="#3A4260",
            fg=TEXT_COLOR,
            activebackground=HOVER_COLOR,
            activeforeground=TEXT_COLOR,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.get_smart_suggestion
        )

        self.suggestion_button.pack(
            fill="x",
            padx=20,
            pady=(0, 10),
            ipady=8
        )


        # ====================================================
        # BUTTON FRAME
        # ====================================================

        button_frame = tk.Frame(
            self.control_panel,
            bg=CARD_COLOR
        )

        button_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )


        # ====================================================
        # GENERATE
        # ====================================================

        self.generate_button = tk.Button(
            button_frame,
            text="📈 Generate Chart",
            font=("Segoe UI", 10, "bold"),
            bg=ACCENT_COLOR,
            fg=TEXT_COLOR,
            activebackground=HOVER_COLOR,
            activeforeground=TEXT_COLOR,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.generate_chart
        )

        self.generate_button.pack(
            fill="x",
            pady=(0, 8),
            ipady=8
        )


        # ====================================================
        # CLEAR
        # ====================================================

        self.clear_button = tk.Button(
            button_frame,
            text="✕ Clear",
            font=("Segoe UI", 10, "bold"),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            activebackground="#303A4E",
            activeforeground=TEXT_COLOR,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.clear_chart
        )

        self.clear_button.pack(
            fill="x",
            pady=(0, 8),
            ipady=8
        )


        # ====================================================
        # SAVE
        # ====================================================

        self.save_button = tk.Button(
            button_frame,
            text="💾 Save Chart",
            font=("Segoe UI", 10, "bold"),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            activebackground="#303A4E",
            activeforeground=TEXT_COLOR,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.save_chart
        )

        self.save_button.pack(
            fill="x",
            ipady=8
        )


        # ====================================================
        # STATUS
        # ====================================================

        self.status_label = tk.Label(
            self.control_panel,
            text="No data loaded",
            font=("Segoe UI", 8),
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT,
            wraplength=270,
            justify="left"
        )

        self.status_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )


        # ====================================================
        # RIGHT CHART PANEL
        # ====================================================

        chart_panel = tk.Frame(
            content,
            bg=CARD_COLOR
        )

        chart_panel.pack(
            side="right",
            fill="both",
            expand=True
        )


        # ====================================================
        # CHART HEADER
        # ====================================================

        chart_header = tk.Frame(
            chart_panel,
            bg=CARD_COLOR
        )

        chart_header.pack(
            fill="x",
            padx=20,
            pady=(15, 10)
        )


        tk.Label(
            chart_header,
            text="Chart Preview",
            font=("Segoe UI", 15, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            side="left"
        )


        self.chart_status = tk.Label(
            chart_header,
            text="No chart generated",
            font=("Segoe UI", 9),
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT
        )

        self.chart_status.pack(
            side="right"
        )


        # ====================================================
        # CHART AREA
        # ====================================================

        self.chart_area = tk.Frame(
            chart_panel,
            bg=INPUT_COLOR
        )

        self.chart_area.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )


        self.show_empty_chart()


    # ========================================================
    # SCROLL FUNCTIONS
    # ========================================================

    def update_control_scroll(self, event=None):

        self.control_canvas.configure(
            scrollregion=self.control_canvas.bbox("all")
        )


    def resize_control_panel(self, event):

        self.control_canvas.itemconfig(
            self.control_window,
            width=event.width
        )


    def mousewheel_scroll(self, event):

        try:

            if event.widget.winfo_toplevel() == self.parent.winfo_toplevel():

                self.control_canvas.yview_scroll(
                    int(-1 * (event.delta / 120)),
                    "units"
                )

        except Exception:
            pass


    # ========================================================
    # SELECT DATABASE
    # ========================================================

    def select_database(self):

        path = filedialog.askopenfilename(
            title="Select Data File",
            filetypes=[
                (
                    "Supported Data Files",
                    "*.db *.sqlite *.sqlite3 *.csv *.xlsx *.xls *.json"
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
                    "All Files",
                    "*.*"
                )
            ]
        )

        if not path:
            return

        self.database_entry.delete(
            0,
            tk.END
        )

        self.database_entry.insert(
            0,
            path
        )

        self.load_database(
            path
        )


    # ========================================================
    # LOAD DATABASE
    # ========================================================

    def load_database(self, path):

        try:

            extension = os.path.splitext(
                path
            )[1].lower()

            self.db_path = path

            if self.connection:

                try:
                    self.connection.close()
                except Exception:
                    pass

                self.connection = None


            self.dataframe = None
            self.tables = []
            self.columns = []


            # =================================================
            # SQLITE
            # =================================================

            if extension in (
                ".db",
                ".sqlite",
                ".sqlite3"
            ):

                self.connection = sqlite3.connect(
                    path
                )

                self.load_sqlite_tables()


            # =================================================
            # CSV
            # =================================================

            elif extension == ".csv":

                self.require_pandas()

                self.dataframe = pd.read_csv(
                    path
                )

                self.create_memory_database()


            # =================================================
            # EXCEL
            # =================================================

            elif extension in (
                ".xlsx",
                ".xls"
            ):

                self.require_pandas()

                self.dataframe = pd.read_excel(
                    path
                )

                self.create_memory_database()


            # =================================================
            # JSON
            # =================================================

            elif extension == ".json":

                self.require_pandas()

                self.dataframe = pd.read_json(
                    path
                )

                self.create_memory_database()


            else:

                raise Exception(
                    "Unsupported file type."
                )


            self.status_label.config(
                text=(
                    "Data loaded successfully.\n"
                    "Click 'Get Suggestion' for smart analysis."
                ),
                fg=SUCCESS_COLOR
            )


            self.chart_status.config(
                text="Data ready",
                fg=SUCCESS_COLOR
            )


            self.suggestion_label.config(
                text=(
                    "Your file is loaded.\n\n"
                    "Click '💡 Get Suggestion' and "
                    "the system will analyze your columns."
                )
            )


        except Exception as error:

            self.status_label.config(
                text="Failed to load data.",
                fg=DANGER_COLOR
            )

            messagebox.showerror(
                "Data Loading Error",
                str(error)
            )


    # ========================================================
    # REQUIRE PANDAS
    # ========================================================

    def require_pandas(self):

        if pd is None:

            raise Exception(
                "Pandas is required.\n\n"
                "Install using:\n"
                "pip install pandas openpyxl"
            )


    # ========================================================
    # CREATE MEMORY DATABASE
    # ========================================================

    def create_memory_database(self):

        if self.dataframe is None:
            return

        if self.dataframe.empty:

            raise Exception(
                "Selected file contains no data."
            )


        self.connection = sqlite3.connect(
            ":memory:"
        )


        self.dataframe.to_sql(
            "data",
            self.connection,
            index=False,
            if_exists="replace"
        )


        self.tables = [
            "data"
        ]


        self.table_combo["values"] = self.tables

        self.table_combo.current(0)

        self.current_table = "data"

        self.load_columns()


    # ========================================================
    # LOAD SQLITE TABLES
    # ========================================================

    def load_sqlite_tables(self):

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


        self.table_combo["values"] = self.tables


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

                self.table_combo.current(0)

                self.current_table = self.tables[0]


            self.load_columns()


        else:

            self.table_combo.set("")

            self.columns = []


    # ========================================================
    # TABLE CHANGED
    # ========================================================

    def table_changed(self, event=None):

        table = self.table_combo.get().strip()

        if not table:
            return

        self.current_table = table

        self.load_columns()


        self.suggestion_label.config(
            text=(
                "Table changed.\n\n"
                "Click '💡 Get Suggestion' to analyze "
                "this table."
            )
        )


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


            self.x_combo["values"] = self.columns
            self.y_combo["values"] = self.columns


            if self.columns:

                self.x_var.set(
                    self.columns[0]
                )


            if len(self.columns) > 1:

                self.y_var.set(
                    self.columns[1]
                )

            elif self.columns:

                self.y_var.set(
                    self.columns[0]
                )


            self.status_label.config(
                text=(
                    f"Table: {self.current_table}\n"
                    f"Columns: {len(self.columns)}"
                ),
                fg=SECONDARY_TEXT
            )


        except Exception as error:

            messagebox.showerror(
                "Column Error",
                str(error)
            )


    # ========================================================
    # GET DATA
    # ========================================================

    def get_data(self):

        if not self.connection:

            raise Exception(
                "Please select a data file first."
            )


        if not self.current_table:

            raise Exception(
                "Please select a table."
            )


        query = (
            f'SELECT * FROM '
            f'"{self.current_table}" '
            f'LIMIT 10000'
        )


        if pd is not None:

            return pd.read_sql_query(
                query,
                self.connection
            )


        cursor = self.connection.cursor()

        cursor.execute(
            query
        )

        rows = cursor.fetchall()

        columns = [
            description[0]
            for description in cursor.description
        ]

        return rows, columns


    # ========================================================
    # COLUMN ANALYSIS
    # ========================================================

    def analyze_columns(self, df):

        numeric_columns = []

        categorical_columns = []

        date_columns = []

        for column in df.columns:

            series = df[column]

            # Numeric
            if pd.api.types.is_numeric_dtype(series):

                numeric_columns.append(
                    column
                )

                continue


            # Date
            try:

                converted = pd.to_datetime(
                    series,
                    errors="coerce"
                )

                ratio = converted.notna().mean()

                if ratio >= 0.70:

                    date_columns.append(
                        column
                    )

                    continue

            except Exception:
                pass


            # Categorical
            categorical_columns.append(
                column
            )


        return (
            numeric_columns,
            categorical_columns,
            date_columns
        )


    # ========================================================
    # SMART SUGGESTION
    # ========================================================

    def get_smart_suggestion(self):

        if pd is None:

            messagebox.showerror(
                "Pandas Required",
                "Install pandas first:\n\n"
                "pip install pandas"
            )

            return


        if not self.connection:

            messagebox.showwarning(
                "Data Required",
                "Please upload/select a data file first."
            )

            return


        try:

            df = self.get_data()


            if df.empty:

                raise Exception(
                    "The selected table contains no data."
                )


            numeric_columns, categorical_columns, date_columns = (
                self.analyze_columns(df)
            )


            row_count = len(df)

            column_count = len(df.columns)


            # =================================================
            # DATE + NUMERIC
            # =================================================

            if date_columns and numeric_columns:

                x_column = date_columns[0]

                y_column = numeric_columns[0]

                chart = "Line"

                aggregation = "Sum"

                explanation = (
                    f"Best choice: Line Chart\n\n"
                    f"X-axis: {x_column}\n"
                    f"Y-axis: {y_column}\n"
                    f"Aggregation: Sum\n\n"
                    f"Reason:\n"
                    f"{x_column} appears to contain dates "
                    f"and {y_column} is numeric. "
                    f"A line chart is ideal for showing "
                    f"trends over time."
                )


            # =================================================
            # CATEGORY + NUMERIC
            # =================================================

            elif categorical_columns and numeric_columns:

                x_column = categorical_columns[0]

                y_column = numeric_columns[0]

                unique_count = df[
                    x_column
                ].nunique()


                if unique_count <= 8:

                    chart = "Pie"

                    aggregation = "Sum"

                    explanation = (
                        f"Best choice: Pie Chart\n\n"
                        f"X-axis: {x_column}\n"
                        f"Y-axis: {y_column}\n"
                        f"Aggregation: Sum\n\n"
                        f"Reason:\n"
                        f"{x_column} contains only "
                        f"{unique_count} categories, "
                        f"so a pie chart can clearly "
                        f"show their proportions."
                    )

                else:

                    chart = "Bar"

                    aggregation = "Sum"

                    explanation = (
                        f"Best choice: Bar Chart\n\n"
                        f"X-axis: {x_column}\n"
                        f"Y-axis: {y_column}\n"
                        f"Aggregation: Sum\n\n"
                        f"Reason:\n"
                        f"{x_column} contains "
                        f"{unique_count} categories. "
                        f"A bar chart is easier to compare "
                        f"than a pie chart."
                    )


                if unique_count > 20:

                    top_n = "Top 10"

                elif unique_count > 10:

                    top_n = "Top 20"

                else:

                    top_n = "All"


            # =================================================
            # TWO NUMERIC COLUMNS
            # =================================================

            elif len(numeric_columns) >= 2:

                x_column = numeric_columns[0]

                y_column = numeric_columns[1]

                chart = "Scatter"

                aggregation = "Sum"

                top_n = "All"

                explanation = (
                    f"Best choice: Scatter Chart\n\n"
                    f"X-axis: {x_column}\n"
                    f"Y-axis: {y_column}\n\n"
                    f"Reason:\n"
                    f"Your file contains multiple numeric "
                    f"columns. A scatter chart is useful "
                    f"for examining the relationship between "
                    f"two numeric variables."
                )


            # =================================================
            # ONE NUMERIC COLUMN
            # =================================================

            elif len(numeric_columns) == 1:

                x_column = numeric_columns[0]

                y_column = numeric_columns[0]

                chart = "Histogram"

                aggregation = "Sum"

                top_n = "All"

                explanation = (
                    f"Best choice: Histogram\n\n"
                    f"Column: {x_column}\n\n"
                    f"Reason:\n"
                    f"Your dataset contains a numeric "
                    f"column but no suitable categorical "
                    f"dimension. A histogram is useful "
                    f"for understanding its distribution."
                )


            # =================================================
            # ONLY CATEGORICAL
            # =================================================

            elif categorical_columns:

                x_column = categorical_columns[0]

                y_column = categorical_columns[0]

                chart = "Bar"

                aggregation = "Count"

                top_n = "Top 10"

                explanation = (
                    f"Best choice: Bar Chart\n\n"
                    f"X-axis: {x_column}\n"
                    f"Y-axis: {x_column}\n"
                    f"Aggregation: Count\n\n"
                    f"Reason:\n"
                    f"The dataset mainly contains "
                    f"categorical information. "
                    f"A count-based bar chart shows "
                    f"how frequently each category occurs."
                )


            else:

                raise Exception(
                    "Unable to determine a suitable "
                    "visualization for this dataset."
                )


            # =================================================
            # DEFAULT TOP N
            # =================================================

            if "top_n" not in locals():

                top_n = "All"


            # =================================================
            # APPLY SUGGESTION
            # =================================================

            self.chart_type.set(
                chart
            )

            self.x_var.set(
                x_column
            )

            self.y_var.set(
                y_column
            )

            self.aggregation_var.set(
                aggregation
            )

            self.top_n_var.set(
                top_n
            )


            # Save suggestion
            self.suggestion_data = {
                "chart": chart,
                "x": x_column,
                "y": y_column,
                "aggregation": aggregation,
                "top_n": top_n
            }


            # =================================================
            # UPDATE UI
            # =================================================

            self.suggestion_label.config(
                text=(
                    explanation
                    + "\n\n"
                    + f"Dataset: {row_count:,} rows × "
                    + f"{column_count} columns"
                ),
                fg=TEXT_COLOR
            )


            self.status_label.config(
                text=(
                    f"Smart suggestion generated.\n"
                    f"Recommended: {chart}"
                ),
                fg=SUCCESS_COLOR
            )


            self.chart_status.config(
                text=f"Suggestion: {chart}",
                fg=WARNING_COLOR
            )


            self.chart_type_changed()


        except Exception as error:

            messagebox.showerror(
                "Suggestion Error",
                str(error)
            )


    # ========================================================
    # CHART TYPE CHANGED
    # ========================================================

    def chart_type_changed(self, event=None):

        selected = self.chart_type.get()


        if selected == "Histogram":

            self.x_combo.config(
                state="disabled"
            )

            self.y_combo.config(
                state="readonly"
            )

            self.aggregation_combo.config(
                state="disabled"
            )

            self.top_n_combo.config(
                state="disabled"
            )


        elif selected == "Scatter":

            self.x_combo.config(
                state="readonly"
            )

            self.y_combo.config(
                state="readonly"
            )

            self.aggregation_combo.config(
                state="disabled"
            )

            self.top_n_combo.config(
                state="disabled"
            )


        else:

            self.x_combo.config(
                state="readonly"
            )

            self.y_combo.config(
                state="readonly"
            )

            self.aggregation_combo.config(
                state="readonly"
            )

            self.top_n_combo.config(
                state="readonly"
            )


    # ========================================================
    # PREPARE DATA
    # ========================================================

    def prepare_chart_data(
        self,
        df,
        x_column,
        y_column,
        aggregation
    ):

        working = df[
            [
                x_column,
                y_column
            ]
        ].copy()


        working[y_column] = pd.to_numeric(
            working[y_column],
            errors="coerce"
        )


        working = working.dropna(
            subset=[
                x_column,
                y_column
            ]
        )


        if working.empty:

            raise Exception(
                "Selected columns do not contain usable data."
            )


        # ====================================================
        # AGGREGATION
        # ====================================================

        if aggregation == "Sum":

            result = working.groupby(
                x_column
            )[y_column].sum()

        elif aggregation == "Average":

            result = working.groupby(
                x_column
            )[y_column].mean()

        elif aggregation == "Count":

            result = working.groupby(
                x_column
            )[y_column].count()

        elif aggregation == "Minimum":

            result = working.groupby(
                x_column
            )[y_column].min()

        elif aggregation == "Maximum":

            result = working.groupby(
                x_column
            )[y_column].max()

        else:

            result = working.groupby(
                x_column
            )[y_column].sum()


        return result.sort_values(
            ascending=False
        )


    # ========================================================
    # TOP N
    # ========================================================

    def apply_top_n(
        self,
        series
    ):

        value = self.top_n_var.get()

        if value == "Top 5":

            return series.head(5)

        if value == "Top 10":

            return series.head(10)

        if value == "Top 20":

            return series.head(20)

        return series


    # ========================================================
    # GENERATE CHART
    # ========================================================

    def generate_chart(self):

        if plt is None:

            messagebox.showerror(
                "Matplotlib Required",
                "Install matplotlib:\n\n"
                "pip install matplotlib"
            )

            return


        if pd is None:

            messagebox.showerror(
                "Pandas Required",
                "Install pandas:\n\n"
                "pip install pandas"
            )

            return


        if not self.connection:

            messagebox.showwarning(
                "Data Required",
                "Please select a data file first."
            )

            return


        try:

            df = self.get_data()


            if df.empty:

                raise Exception(
                    "The selected table contains no data."
                )


            chart_type = self.chart_type.get()


            # =================================================
            # CLEAR
            # =================================================

            self.clear_chart_area(
                show_message=False
            )


            # =================================================
            # FIGURE
            # =================================================

            self.figure = plt.Figure(
                figsize=(9, 6),
                dpi=100
            )


            axis = self.figure.add_subplot(
                111
            )


            self.figure.patch.set_facecolor(
                CARD_COLOR
            )

            axis.set_facecolor(
                INPUT_COLOR
            )


            # =================================================
            # HISTOGRAM
            # =================================================

            if chart_type == "Histogram":

                column = self.y_var.get()

                numeric_data = pd.to_numeric(
                    df[column],
                    errors="coerce"
                ).dropna()


                if numeric_data.empty:

                    raise Exception(
                        "Histogram requires a numeric column."
                    )


                axis.hist(
                    numeric_data,
                    bins=20,
                    edgecolor="white"
                )


                axis.set_xlabel(
                    column
                )

                axis.set_ylabel(
                    "Frequency"
                )

                axis.set_title(
                    f"Distribution of {column}",
                    fontsize=14,
                    fontweight="bold"
                )


            # =================================================
            # SCATTER
            # =================================================

            elif chart_type == "Scatter":

                x_column = self.x_var.get()

                y_column = self.y_var.get()


                x_numeric = pd.to_numeric(
                    df[x_column],
                    errors="coerce"
                )

                y_numeric = pd.to_numeric(
                    df[y_column],
                    errors="coerce"
                )


                valid = (
                    x_numeric.notna()
                    &
                    y_numeric.notna()
                )


                if not valid.any():

                    raise Exception(
                        "Scatter chart requires numeric X and Y columns."
                    )


                axis.scatter(
                    x_numeric.loc[valid],
                    y_numeric.loc[valid],
                    alpha=0.75
                )


                axis.set_xlabel(
                    x_column
                )

                axis.set_ylabel(
                    y_column
                )

                axis.set_title(
                    f"{y_column} vs {x_column}",
                    fontsize=14,
                    fontweight="bold"
                )


            # =================================================
            # OTHER CHARTS
            # =================================================

            else:

                x_column = self.x_var.get()

                y_column = self.y_var.get()


                if not x_column:

                    raise Exception(
                        "Select an X-axis column."
                    )


                if not y_column:

                    raise Exception(
                        "Select a Y-axis column."
                    )


                aggregation = (
                    self.aggregation_var.get()
                )


                series = self.prepare_chart_data(
                    df,
                    x_column,
                    y_column,
                    aggregation
                )


                # =================================================
                # SORT DATE
                # =================================================

                try:

                    converted = pd.to_datetime(
                        series.index,
                        errors="coerce"
                    )

                    if converted.notna().mean() >= 0.7:

                        series.index = converted

                        series = series.sort_index()

                except Exception:
                    pass


                # =================================================
                # TOP N
                # =================================================

                if chart_type in (
                    "Bar",
                    "Pie"
                ):

                    series = self.apply_top_n(
                        series
                    )


                x_values = series.index

                y_values = series.values


                # =================================================
                # BAR
                # =================================================

                if chart_type == "Bar":

                    labels = [
                        str(value)
                        for value in x_values
                    ]


                    bars = axis.bar(
                        range(len(labels)),
                        y_values
                    )


                    axis.set_xticks(
                        range(len(labels))
                    )


                    axis.set_xticklabels(
                        labels,
                        rotation=35,
                        ha="right"
                    )


                    axis.set_xlabel(
                        x_column
                    )


                    axis.set_ylabel(
                        f"{aggregation} of {y_column}"
                    )


                    axis.set_title(
                        f"{aggregation} {y_column} by {x_column}",
                        fontsize=14,
                        fontweight="bold"
                    )


                    if len(bars) <= 20:

                        for bar, value in zip(
                            bars,
                            y_values
                        ):

                            axis.text(
                                bar.get_x()
                                + bar.get_width() / 2,
                                bar.get_height(),
                                f"{value:,.0f}",
                                ha="center",
                                va="bottom",
                                fontsize=8
                            )


                # =================================================
                # LINE
                # =================================================

                elif chart_type == "Line":

                    axis.plot(
                        range(len(y_values)),
                        y_values,
                        marker="o",
                        linewidth=2
                    )


                    labels = [
                        str(value)
                        for value in x_values
                    ]


                    step = max(
                        1,
                        len(labels) // 12
                    )


                    visible_positions = list(
                        range(
                            0,
                            len(labels),
                            step
                        )
                    )


                    axis.set_xticks(
                        visible_positions
                    )


                    axis.set_xticklabels(
                        [
                            labels[i]
                            for i in visible_positions
                        ],
                        rotation=35,
                        ha="right"
                    )


                    axis.set_xlabel(
                        x_column
                    )

                    axis.set_ylabel(
                        f"{aggregation} of {y_column}"
                    )


                    axis.set_title(
                        f"{aggregation} {y_column} by {x_column}",
                        fontsize=14,
                        fontweight="bold"
                    )


                # =================================================
                # AREA
                # =================================================

                elif chart_type == "Area":

                    positions = range(
                        len(y_values)
                    )


                    axis.fill_between(
                        positions,
                        y_values,
                        alpha=0.35
                    )


                    axis.plot(
                        positions,
                        y_values,
                        linewidth=2
                    )


                    labels = [
                        str(value)
                        for value in x_values
                    ]


                    step = max(
                        1,
                        len(labels) // 12
                    )


                    visible_positions = list(
                        range(
                            0,
                            len(labels),
                            step
                        )
                    )


                    axis.set_xticks(
                        visible_positions
                    )


                    axis.set_xticklabels(
                        [
                            labels[i]
                            for i in visible_positions
                        ],
                        rotation=35,
                        ha="right"
                    )


                    axis.set_xlabel(
                        x_column
                    )

                    axis.set_ylabel(
                        f"{aggregation} of {y_column}"
                    )


                    axis.set_title(
                        f"{aggregation} {y_column} by {x_column}",
                        fontsize=14,
                        fontweight="bold"
                    )


                # =================================================
                # PIE
                # =================================================

                elif chart_type == "Pie":

                    if len(series) > 20:

                        series = series.head(20)


                    axis.pie(
                        series.values,
                        labels=[
                            str(value)
                            for value in series.index
                        ],
                        autopct="%1.1f%%",
                        startangle=90
                    )


                    axis.set_title(
                        f"{aggregation} {y_column} by {x_column}",
                        fontsize=14,
                        fontweight="bold"
                    )


                # =================================================
                # GRID
                # =================================================

                if chart_type != "Pie":

                    axis.grid(
                        True,
                        alpha=0.15
                    )


            # =================================================
            # LAYOUT
            # =================================================

            self.figure.tight_layout()


            # =================================================
            # CANVAS
            # =================================================

            self.canvas = FigureCanvasTkAgg(
                self.figure,
                master=self.chart_area
            )


            self.canvas.draw()


            self.canvas.get_tk_widget().pack(
                fill="both",
                expand=True,
                padx=10,
                pady=10
            )


            # =================================================
            # STATUS
            # =================================================

            self.chart_status.config(
                text=f"{chart_type} chart generated",
                fg=SUCCESS_COLOR
            )


            self.status_label.config(
                text=(
                    f"Chart generated successfully.\n"
                    f"Type: {chart_type}\n"
                    f"Rows analyzed: {len(df):,}"
                ),
                fg=SUCCESS_COLOR
            )


        except Exception as error:

            self.chart_status.config(
                text="Chart generation failed",
                fg=DANGER_COLOR
            )


            messagebox.showerror(
                "Chart Error",
                str(error)
            )


    # ========================================================
    # SAVE CHART
    # ========================================================

    def save_chart(self):

        if self.figure is None:

            messagebox.showwarning(
                "No Chart",
                "Generate a chart before saving it."
            )

            return


        path = filedialog.asksaveasfilename(
            title="Save Chart",
            defaultextension=".png",
            filetypes=[
                (
                    "PNG Image",
                    "*.png"
                ),
                (
                    "JPG Image",
                    "*.jpg"
                ),
                (
                    "PDF File",
                    "*.pdf"
                )
            ]
        )


        if not path:
            return


        try:

            self.figure.savefig(
                path,
                dpi=300,
                bbox_inches="tight",
                facecolor=self.figure.get_facecolor()
            )


            self.status_label.config(
                text="Chart saved successfully.",
                fg=SUCCESS_COLOR
            )


            messagebox.showinfo(
                "Chart Saved",
                f"Chart saved successfully:\n\n{path}"
            )


        except Exception as error:

            messagebox.showerror(
                "Save Error",
                str(error)
            )


    # ========================================================
    # CLEAR CHART
    # ========================================================

    def clear_chart(self):

        self.clear_chart_area(
            show_message=True
        )


        self.chart_type.set(
            "Bar"
        )


        self.aggregation_var.set(
            "Sum"
        )


        self.top_n_var.set(
            "All"
        )


        self.chart_type_changed()


        if self.columns:

            self.x_var.set(
                self.columns[0]
            )


            if len(self.columns) > 1:

                self.y_var.set(
                    self.columns[1]
                )

            else:

                self.y_var.set(
                    self.columns[0]
                )


        else:

            self.x_var.set("")
            self.y_var.set("")


        self.suggestion_label.config(
            text=(
                "Chart cleared.\n\n"
                "Click '💡 Get Suggestion' "
                "to analyze your data again."
            ),
            fg=SECONDARY_TEXT
        )


        self.status_label.config(
            text="Chart cleared.",
            fg=SECONDARY_TEXT
        )


    # ========================================================
    # CLEAR CHART AREA
    # ========================================================

    def clear_chart_area(
        self,
        show_message=True
    ):

        for widget in self.chart_area.winfo_children():

            widget.destroy()


        if self.figure is not None:

            try:

                plt.close(
                    self.figure
                )

            except Exception:
                pass


        self.figure = None

        self.canvas = None


        if show_message:

            self.show_empty_chart()


    # ========================================================
    # EMPTY CHART
    # ========================================================

    def show_empty_chart(self):

        for widget in self.chart_area.winfo_children():

            widget.destroy()


        empty_frame = tk.Frame(
            self.chart_area,
            bg=INPUT_COLOR
        )


        empty_frame.pack(
            fill="both",
            expand=True
        )


        tk.Label(
            empty_frame,
            text="📊",
            font=("Segoe UI", 42),
            bg=INPUT_COLOR,
            fg=ACCENT_COLOR
        ).pack(
            pady=(100, 10)
        )


        tk.Label(
            empty_frame,
            text="No chart generated",
            font=("Segoe UI", 15, "bold"),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR
        ).pack()


        tk.Label(
            empty_frame,
            text=(
                "Upload your data → Get Suggestion → "
                "Generate Chart"
            ),
            font=("Segoe UI", 10),
            bg=INPUT_COLOR,
            fg=SECONDARY_TEXT,
            justify="center"
        ).pack(
            pady=8
        )


        self.chart_status.config(
            text="No chart generated",
            fg=SECONDARY_TEXT
        )


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
        "AI SQL Studio - Data Visualization"
    )

    root.geometry(
        "1350x850"
    )

    root.minsize(
        1100,
        700
    )

    root.configure(
        bg=BG_COLOR
    )


    Visualization(
        root
    )


    root.mainloop()