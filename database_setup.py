# ============================================================
# DATABASE_SETUP.PY
# Multi-Format Data Setup
# ============================================================

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from data_loader import DataLoader


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

SUCCESS_COLOR = "#06D6A0"
DANGER_COLOR = "#FF6B6B"
WARNING_COLOR = "#FFD166"


# ============================================================
# DATABASE SETUP
# ============================================================

class DatabaseSetup:

    def __init__(self, parent):

        self.parent = parent

        # Keep one DataLoader object alive
        self.loader = DataLoader()

        self.selected_file = None
        self.selected_table = None

        self.current_dataframe = None

        self.create_ui()


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
        # HEADER
        # ====================================================

        header = tk.Frame(
            self.parent,
            bg=BG_COLOR
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(25, 10)
        )


        tk.Label(
            header,
            text="Database Setup",
            font=("Segoe UI", 26, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w"
        )


        tk.Label(
            header,
            text="Load and analyze your data from multiple file formats",
            font=("Segoe UI", 10),
            bg=BG_COLOR,
            fg=SECONDARY_TEXT
        ).pack(
            anchor="w",
            pady=(5, 0)
        )


        # ====================================================
        # FILE CARD
        # ====================================================

        file_card = tk.Frame(
            self.parent,
            bg=CARD_COLOR
        )

        file_card.pack(
            fill="x",
            padx=30,
            pady=15
        )


        tk.Label(
            file_card,
            text="Data Source",
            font=("Segoe UI", 13, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 10)
        )


        # ====================================================
        # FILE PATH
        # ====================================================

        file_row = tk.Frame(
            file_card,
            bg=CARD_COLOR
        )

        file_row.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )


        self.file_entry = tk.Entry(
            file_row,
            font=("Segoe UI", 10),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            relief="flat",
            bd=0
        )

        self.file_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=10
        )


        browse_button = tk.Button(
            file_row,
            text="Select File",
            font=("Segoe UI", 10, "bold"),
            bg=ACCENT_COLOR,
            fg=TEXT_COLOR,
            activebackground=HOVER_COLOR,
            activeforeground=TEXT_COLOR,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.select_file
        )

        browse_button.pack(
            side="right",
            padx=(10, 0),
            ipadx=15,
            ipady=7
        )


        # ====================================================
        # SUPPORTED FILES
        # ====================================================

        tk.Label(
            file_card,
            text="Supported: SQLite • CSV • Excel • JSON",
            font=("Segoe UI", 9),
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 10)
        )


        # ====================================================
        # ACTION BUTTONS
        # ====================================================

        action_frame = tk.Frame(
            file_card,
            bg=CARD_COLOR
        )

        action_frame.pack(
            fill="x",
            padx=20,
            pady=(5, 18)
        )


        # ----------------------------------------------------
        # GENERATE SQL
        # ----------------------------------------------------

        generate_sql_button = tk.Button(
            action_frame,
            text="⚡ Generate SQL",
            font=("Segoe UI", 10, "bold"),
            bg=ACCENT_COLOR,
            fg=TEXT_COLOR,
            activebackground=HOVER_COLOR,
            activeforeground=TEXT_COLOR,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.open_sql_generator
        )

        generate_sql_button.pack(
            side="left",
            ipadx=18,
            ipady=8
        )


        # ----------------------------------------------------
        # CLEAR
        # ----------------------------------------------------

        clear_button = tk.Button(
            action_frame,
            text="✕ Clear",
            font=("Segoe UI", 10, "bold"),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            activebackground="#303A4E",
            activeforeground=TEXT_COLOR,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.clear_data
        )

        clear_button.pack(
            side="left",
            padx=(10, 0),
            ipadx=18,
            ipady=8
        )


        # ====================================================
        # DATABASE INFORMATION
        # ====================================================

        info_frame = tk.Frame(
            self.parent,
            bg=BG_COLOR
        )

        info_frame.pack(
            fill="x",
            padx=30,
            pady=5
        )


        # ====================================================
        # TABLE CARD
        # ====================================================

        table_card = tk.Frame(
            info_frame,
            bg=CARD_COLOR
        )

        table_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 5)
        )


        tk.Label(
            table_card,
            text="Tables",
            font=("Segoe UI", 11, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 8)
        )


        self.table_combo = ttk.Combobox(
            table_card,
            state="readonly",
            font=("Segoe UI", 10)
        )

        self.table_combo.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )


        self.table_combo.bind(
            "<<ComboboxSelected>>",
            self.table_selected
        )


        # ====================================================
        # SOURCE TYPE
        # ====================================================

        type_card = tk.Frame(
            info_frame,
            bg=CARD_COLOR
        )

        type_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )


        tk.Label(
            type_card,
            text="Source Type",
            font=("Segoe UI", 11, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )


        self.type_label = tk.Label(
            type_card,
            text="Not selected",
            font=("Segoe UI", 11),
            bg=CARD_COLOR,
            fg=ACCENT_COLOR
        )

        self.type_label.pack(
            anchor="w",
            padx=15,
            pady=(0, 15)
        )


        # ====================================================
        # ROW COUNT
        # ====================================================

        rows_card = tk.Frame(
            info_frame,
            bg=CARD_COLOR
        )

        rows_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )


        tk.Label(
            rows_card,
            text="Rows",
            font=("Segoe UI", 11, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )


        self.rows_label = tk.Label(
            rows_card,
            text="0",
            font=("Segoe UI", 11),
            bg=CARD_COLOR,
            fg=ACCENT_COLOR
        )

        self.rows_label.pack(
            anchor="w",
            padx=15,
            pady=(0, 15)
        )


        # ====================================================
        # NULL COUNT
        # ====================================================

        null_card = tk.Frame(
            info_frame,
            bg=CARD_COLOR
        )

        null_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )


        tk.Label(
            null_card,
            text="NULL Values",
            font=("Segoe UI", 11, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )


        self.null_label = tk.Label(
            null_card,
            text="0",
            font=("Segoe UI", 11),
            bg=CARD_COLOR,
            fg=WARNING_COLOR
        )

        self.null_label.pack(
            anchor="w",
            padx=15,
            pady=(0, 15)
        )


        # ====================================================
        # DUPLICATE COUNT
        # ====================================================

        duplicate_card = tk.Frame(
            info_frame,
            bg=CARD_COLOR
        )

        duplicate_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(5, 0)
        )


        tk.Label(
            duplicate_card,
            text="Duplicates",
            font=("Segoe UI", 11, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )


        self.duplicate_label = tk.Label(
            duplicate_card,
            text="0",
            font=("Segoe UI", 11),
            bg=CARD_COLOR,
            fg=DANGER_COLOR
        )

        self.duplicate_label.pack(
            anchor="w",
            padx=15,
            pady=(0, 15)
        )


        # ====================================================
        # DATA CARD
        # ====================================================

        data_card = tk.Frame(
            self.parent,
            bg=CARD_COLOR
        )

        data_card.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(15, 30)
        )


        # ====================================================
        # DATA HEADER
        # ====================================================

        data_header = tk.Frame(
            data_card,
            bg=CARD_COLOR
        )

        data_header.pack(
            fill="x"
        )


        tk.Label(
            data_header,
            text="Data Preview",
            font=("Segoe UI", 14, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            side="left",
            padx=20,
            pady=15
        )


        self.status_label = tk.Label(
            data_header,
            text="No file loaded",
            font=("Segoe UI", 9),
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT
        )

        self.status_label.pack(
            side="right",
            padx=20
        )


        # ====================================================
        # TREE AREA
        # ====================================================

        tree_frame = tk.Frame(
            data_card,
            bg=CARD_COLOR
        )

        tree_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 5)
        )


        # ====================================================
        # TREEVIEW
        # ====================================================

        self.tree = ttk.Treeview(
            tree_frame,
            show="headings"
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )


        # ====================================================
        # VERTICAL SCROLLBAR
        # ====================================================

        vertical_scroll = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=self.tree.yview
        )

        vertical_scroll.pack(
            side="right",
            fill="y"
        )


        self.tree.configure(
            yscrollcommand=vertical_scroll.set
        )


        # ====================================================
        # HORIZONTAL SCROLLBAR
        # ====================================================

        horizontal_scroll = ttk.Scrollbar(
            data_card,
            orient="horizontal",
            command=self.tree.xview
        )

        horizontal_scroll.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )


        self.tree.configure(
            xscrollcommand=horizontal_scroll.set
        )


    # ========================================================
    # SELECT FILE
    # ========================================================

    def select_file(self):

        file_path = filedialog.askopenfilename(
            title="Select Data File",
            filetypes=[
                (
                    "All Supported Files",
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


        if not file_path:
            return


        self.file_entry.delete(
            0,
            tk.END
        )

        self.file_entry.insert(
            0,
            file_path
        )


        self.load_selected_file(
            file_path
        )


    # ========================================================
    # LOAD SELECTED FILE
    # ========================================================

    def load_selected_file(
        self,
        file_path
    ):

        try:

            self.status_label.config(
                text="Loading...",
                fg=WARNING_COLOR
            )

            self.parent.update_idletasks()


            result = self.loader.load_file(
                file_path
            )


            self.selected_file = file_path


            # ------------------------------------------------
            # SOURCE TYPE
            # ------------------------------------------------

            source_type = result["type"].upper()


            self.type_label.config(
                text=source_type,
                fg=SUCCESS_COLOR
            )


            # ------------------------------------------------
            # TABLES
            # ------------------------------------------------

            tables = result["tables"]


            self.table_combo["values"] = tables


            if tables:

                self.table_combo.current(0)

                self.selected_table = tables[0]

                self.show_table_data(
                    tables[0]
                )

            else:

                self.table_combo.set("")

                self.selected_table = None

                self.clear_preview()


            self.status_label.config(
                text="File loaded successfully",
                fg=SUCCESS_COLOR
            )


        except Exception as error:

            self.status_label.config(
                text="Loading failed",
                fg=DANGER_COLOR
            )


            messagebox.showerror(
                "File Loading Error",
                str(error)
            )


    # ========================================================
    # TABLE SELECTED
    # ========================================================

    def table_selected(
        self,
        event=None
    ):

        table_name = self.table_combo.get()


        if not table_name:
            return


        self.selected_table = table_name


        self.show_table_data(
            table_name
        )


    # ========================================================
    # SHOW TABLE DATA
    # ========================================================

    def show_table_data(
        self,
        table_name
    ):

        try:

            # ------------------------------------------------
            # Clear old tree
            # ------------------------------------------------

            self.tree.delete(
                *self.tree.get_children()
            )


            # ------------------------------------------------
            # Get data
            # ------------------------------------------------

            df = self.loader.get_data(
                table_name,
                limit=500
            )


            self.current_dataframe = df


            # ------------------------------------------------
            # ROW COUNT
            # ------------------------------------------------

            self.rows_label.config(
                text=str(len(df))
            )


            # ------------------------------------------------
            # NULL COUNT
            # ------------------------------------------------

            null_count = 0


            try:

                null_count = int(
                    df.isnull().sum().sum()
                )

            except Exception:

                for column in df.columns:

                    for value in df[column]:

                        if pd_is_null(value):

                            null_count += 1


            self.null_label.config(
                text=str(null_count)
            )


            # ------------------------------------------------
            # DUPLICATE COUNT
            # ------------------------------------------------

            duplicate_count = 0


            try:

                duplicate_count = int(
                    df.duplicated().sum()
                )

            except Exception:

                duplicate_count = 0


            self.duplicate_label.config(
                text=str(duplicate_count)
            )


            # ------------------------------------------------
            # EMPTY DATA
            # ------------------------------------------------

            if df.empty:

                self.status_label.config(
                    text="Table contains no data",
                    fg=WARNING_COLOR
                )

                return


            # ------------------------------------------------
            # COLUMNS
            # ------------------------------------------------

            columns = [
                str(column)
                for column in df.columns
            ]


            self.tree["columns"] = columns


            # ------------------------------------------------
            # HEADINGS
            # ------------------------------------------------

            for column in columns:

                self.tree.heading(
                    column,
                    text=column
                )


                self.tree.column(
                    column,
                    width=150,
                    minwidth=80,
                    anchor="w"
                )


            # ------------------------------------------------
            # INSERT DATA
            # ------------------------------------------------

            for _, row in df.iterrows():

                values = []


                for value in row:

                    if pd_is_null(value):

                        values.append(
                            "NULL"
                        )

                    else:

                        values.append(
                            str(value)
                        )


                self.tree.insert(
                    "",
                    "end",
                    values=values
                )


            self.status_label.config(
                text=(
                    f"Showing {len(df)} rows  •  "
                    f"NULL: {null_count}  •  "
                    f"Duplicates: {duplicate_count}"
                ),
                fg=SECONDARY_TEXT
            )


        except Exception as error:

            messagebox.showerror(
                "Display Error",
                str(error)
            )


    # ========================================================
    # CLEAR PREVIEW
    # ========================================================

    def clear_preview(self):

        # Clear TreeView
        self.tree.delete(
            *self.tree.get_children()
        )


        # Remove columns
        self.tree["columns"] = ()


        # Reset information
        self.rows_label.config(
            text="0"
        )


        self.null_label.config(
            text="0"
        )


        self.duplicate_label.config(
            text="0"
        )


        self.type_label.config(
            text="Not selected",
            fg=ACCENT_COLOR
        )


        self.status_label.config(
            text="No file loaded",
            fg=SECONDARY_TEXT
        )


        self.current_dataframe = None


    # ========================================================
    # CLEAR DATA
    # ========================================================

    def clear_data(self):

        # ----------------------------------------------------
        # Clear file entry
        # ----------------------------------------------------

        self.file_entry.delete(
            0,
            tk.END
        )


        # ----------------------------------------------------
        # Reset table
        # ----------------------------------------------------

        self.table_combo.set("")

        self.table_combo["values"] = ()


        # ----------------------------------------------------
        # Reset variables
        # ----------------------------------------------------

        self.selected_file = None
        self.selected_table = None
        self.current_dataframe = None


        # ----------------------------------------------------
        # Clear preview
        # ----------------------------------------------------

        self.clear_preview()


        # ----------------------------------------------------
        # Create fresh loader
        # ----------------------------------------------------

        try:

            self.loader = DataLoader()

        except Exception:

            pass


    # ========================================================
    # OPEN SQL GENERATOR
    # ========================================================

    def open_sql_generator(self):

        # ----------------------------------------------------
        # Check file
        # ----------------------------------------------------

        if not self.selected_file:

            messagebox.showwarning(
                "Data Required",
                "Please select and load a data file first."
            )

            return


        # ----------------------------------------------------
        # Check table
        # ----------------------------------------------------

        if not self.selected_table:

            messagebox.showwarning(
                "Table Required",
                "Please select a table first."
            )

            return


        try:

            # ------------------------------------------------
            # Import QueryBuilder
            # ------------------------------------------------

            from query_builder import QueryBuilder


            # ------------------------------------------------
            # Open SQL Generator
            # ------------------------------------------------

            QueryBuilder(
                self.parent,
                db_path=self.selected_file,
                current_table=self.selected_table
            )


        except Exception as error:

            messagebox.showerror(
                "SQL Generator Error",
                str(error)
            )


# ============================================================
# NULL CHECK
# ============================================================

def pd_is_null(value):

    try:

        # None
        if value is None:

            return True


        # NaN
        result = value != value


        return bool(result)


    except Exception:

        return False


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()


    root.title(
        "AI SQL Studio - Database Setup"
    )


    root.geometry(
        "1250x800"
    )


    root.minsize(
        1000,
        700
    )


    root.configure(
        bg=BG_COLOR
    )


    DatabaseSetup(
        root
    )


    root.mainloop()