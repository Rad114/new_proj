import tkinter as tk
from tkinter import messagebox


# ============================================================
# COLORS
# ============================================================

BG_COLOR = "#101522"
CARD_COLOR = "#1C2433"
INPUT_COLOR = "#252D3D"

TEXT_COLOR = "#FFFFFF"
SECONDARY_TEXT = "#AAB2C0"

ACCENT_COLOR = "#6C63E8"
HOVER_COLOR = "#7A72F5"


# ============================================================
# TOOL EXPLORER
# ============================================================

class ToolExplorer:

    def __init__(self, parent):

        self.parent = parent

        self.create_ui()


    # ========================================================
    # CREATE UI
    # ========================================================

    def create_ui(self):

        self.frame = tk.Frame(
            self.parent,
            bg=BG_COLOR
        )

        self.frame.pack(
            fill="both",
            expand=True
        )


        # ====================================================
        # HEADER
        # ====================================================

        title = tk.Label(
            self.frame,
            text="SQL Tool Explorer",
            font=("Segoe UI", 27, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )

        title.pack(
            anchor="w",
            padx=35,
            pady=(30, 5)
        )


        subtitle = tk.Label(
            self.frame,
            text="Explore SQL commands and understand what they do.",
            font=("Segoe UI", 10),
            bg=BG_COLOR,
            fg=SECONDARY_TEXT
        )

        subtitle.pack(
            anchor="w",
            padx=35,
            pady=(0, 25)
        )


        # ====================================================
        # SEARCH
        # ====================================================

        search_frame = tk.Frame(
            self.frame,
            bg=CARD_COLOR
        )

        search_frame.pack(
            fill="x",
            padx=35,
            pady=(0, 20)
        )


        self.search_entry = tk.Entry(
            search_frame,
            font=("Segoe UI", 11),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            insertbackground="white",
            relief="flat"
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=15,
            pady=15,
            ipady=8
        )

        self.search_entry.insert(
            0,
            "Search SQL command..."
        )


        search_button = tk.Button(
            search_frame,
            text="Search",
            font=("Segoe UI", 10, "bold"),
            bg=ACCENT_COLOR,
            fg="white",
            activebackground=HOVER_COLOR,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.search_tools
        )

        search_button.pack(
            side="right",
            padx=15,
            pady=15,
            ipadx=15,
            ipady=7
        )


        # ====================================================
        # MAIN AREA
        # ====================================================

        main_frame = tk.Frame(
            self.frame,
            bg=BG_COLOR
        )

        main_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 30)
        )


        # ====================================================
        # LEFT COMMAND LIST
        # ====================================================

        left_frame = tk.Frame(
            main_frame,
            bg=CARD_COLOR,
            width=280
        )

        left_frame.pack(
            side="left",
            fill="y",
            padx=(0, 15)
        )

        left_frame.pack_propagate(False)


        list_title = tk.Label(
            left_frame,
            text="SQL Commands",
            font=("Segoe UI", 14, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )

        list_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )


        self.command_list = tk.Listbox(
            left_frame,
            font=("Segoe UI", 10),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            selectbackground=ACCENT_COLOR,
            selectforeground="white",
            relief="flat",
            bd=0,
            highlightthickness=0
        )

        self.command_list.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )


        self.command_list.bind(
            "<<ListboxSelect>>",
            self.show_command
        )


        # ====================================================
        # RIGHT INFORMATION
        # ====================================================

        right_frame = tk.Frame(
            main_frame,
            bg=CARD_COLOR
        )

        right_frame.pack(
            side="right",
            fill="both",
            expand=True
        )


        self.command_title = tk.Label(
            right_frame,
            text="Select a SQL command",
            font=("Segoe UI", 20, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )

        self.command_title.pack(
            anchor="w",
            padx=25,
            pady=(25, 10)
        )


        self.description_box = tk.Text(
            right_frame,
            font=("Segoe UI", 10),
            bg=INPUT_COLOR,
            fg=SECONDARY_TEXT,
            relief="flat",
            bd=0,
            wrap="word"
        )

        self.description_box.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 15)
        )


        self.description_box.config(
            state="disabled"
        )


        # ====================================================
        # LOAD COMMANDS
        # ====================================================

        self.commands = {

            "SELECT": {
                "description":
                    "Used to retrieve data from one or more tables.",
                "example":
                    "SELECT name, salary FROM employees;"
            },

            "INSERT": {
                "description":
                    "Used to add new records to a table.",
                "example":
                    "INSERT INTO employees "
                    "(name, salary) "
                    "VALUES ('John', 50000);"
            },

            "UPDATE": {
                "description":
                    "Used to modify existing records.",
                "example":
                    "UPDATE employees "
                    "SET salary = 60000 "
                    "WHERE id = 1;"
            },

            "DELETE": {
                "description":
                    "Used to delete records from a table.",
                "example":
                    "DELETE FROM employees "
                    "WHERE id = 1;"
            },

            "CREATE TABLE": {
                "description":
                    "Creates a new table in the database.",
                "example":
                    "CREATE TABLE employees "
                    "(id INTEGER PRIMARY KEY, "
                    "name TEXT);"
            },

            "ALTER TABLE": {
                "description":
                    "Changes the structure of an existing table.",
                "example":
                    "ALTER TABLE employees "
                    "ADD COLUMN email TEXT;"
            },

            "DROP TABLE": {
                "description":
                    "Deletes a table and its data from the database.",
                "example":
                    "DROP TABLE employees;"
            },

            "CREATE VIEW": {
                "description":
                    "Creates a virtual table based on a SQL query.",
                "example":
                    "CREATE VIEW employee_view AS "
                    "SELECT name, salary FROM employees;"
            },

            "DROP VIEW": {
                "description":
                    "Deletes an existing database view.",
                "example":
                    "DROP VIEW employee_view;"
            },

            "CREATE INDEX": {
                "description":
                    "Creates an index to improve search performance.",
                "example":
                    "CREATE INDEX idx_name "
                    "ON employees(name);"
            },

            "DROP INDEX": {
                "description":
                    "Deletes an existing index.",
                "example":
                    "DROP INDEX idx_name;"
            },

            "CREATE TRIGGER": {
                "description":
                    "Creates an automatic action that runs when "
                    "a database event occurs.",
                "example":
                    "CREATE TRIGGER log_update "
                    "AFTER UPDATE ON employees "
                    "BEGIN "
                    "INSERT INTO logs(message) "
                    "VALUES ('Employee updated'); "
                    "END;"
            },

            "DROP TRIGGER": {
                "description":
                    "Deletes an existing database trigger.",
                "example":
                    "DROP TRIGGER log_update;"
            },

            "JOIN": {
                "description":
                    "Combines related data from multiple tables.",
                "example":
                    "SELECT customers.name, orders.amount "
                    "FROM customers "
                    "JOIN orders "
                    "ON customers.id = orders.customer_id;"
            },

            "GROUP BY": {
                "description":
                    "Groups rows with the same values together.",
                "example":
                    "SELECT department, COUNT(*) "
                    "FROM employees "
                    "GROUP BY department;"
            },

            "HAVING": {
                "description":
                    "Filters grouped results.",
                "example":
                    "SELECT department, COUNT(*) "
                    "FROM employees "
                    "GROUP BY department "
                    "HAVING COUNT(*) > 5;"
            },

            "ORDER BY": {
                "description":
                    "Sorts query results.",
                "example":
                    "SELECT * FROM employees "
                    "ORDER BY salary DESC;"
            },

            "LIMIT": {
                "description":
                    "Restricts the number of rows returned.",
                "example":
                    "SELECT * FROM employees "
                    "LIMIT 10;"
            },

            "UNION": {
                "description":
                    "Combines results from multiple SELECT queries.",
                "example":
                    "SELECT name FROM employees "
                    "UNION "
                    "SELECT name FROM managers;"
            },

            "WITH / CTE": {
                "description":
                    "Creates a temporary named result that can be "
                    "used inside another SQL query.",
                "example":
                    "WITH high_salary AS "
                    "(SELECT * FROM employees "
                    "WHERE salary > 50000) "
                    "SELECT * FROM high_salary;"
            },

            "TRANSACTION": {
                "description":
                    "Controls a group of database operations "
                    "that should be committed or rolled back together.",
                "example":
                    "BEGIN; "
                    "UPDATE employees SET salary = 60000 "
                    "WHERE id = 1; "
                    "COMMIT;"
            },

            "PRAGMA": {
                "description":
                    "Used to read or change SQLite-specific settings.",
                "example":
                    "PRAGMA foreign_keys = ON;"
            }
        }


        self.load_commands()


    # ========================================================
    # LOAD COMMANDS
    # ========================================================

    def load_commands(self, search=""):

        self.command_list.delete(
            0,
            tk.END
        )


        search = search.lower().strip()


        for command in self.commands:

            if (
                not search
                or search in command.lower()
            ):

                self.command_list.insert(
                    tk.END,
                    command
                )


    # ========================================================
    # SEARCH
    # ========================================================

    def search_tools(self):

        search = self.search_entry.get()

        if search == "Search SQL command...":

            search = ""

        self.load_commands(
            search
        )


    # ========================================================
    # SHOW COMMAND
    # ========================================================

    def show_command(self, event=None):

        selection = self.command_list.curselection()


        if not selection:
            return


        command = self.command_list.get(
            selection[0]
        )


        information = self.commands.get(
            command
        )


        if not information:
            return


        self.command_title.config(
            text=command
        )


        self.description_box.config(
            state="normal"
        )


        self.description_box.delete(
            "1.0",
            tk.END
        )


        text = (
            "DESCRIPTION\n\n"
            + information["description"]
            + "\n\n\n"
            "EXAMPLE\n\n"
            + information["example"]
        )


        self.description_box.insert(
            "1.0",
            text
        )


        self.description_box.config(
            state="disabled"
        )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.title(
        "SQL Tool Explorer"
    )

    root.geometry(
        "1100x700"
    )

    root.configure(
        bg=BG_COLOR
    )

    ToolExplorer(
        root
    )

    root.mainloop()