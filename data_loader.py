# ============================================================
# DATA_LOADER.PY
# Common Data Loader for AI SQL Studio
# ============================================================

import os
import sqlite3
import pandas as pd


# ============================================================
# SUPPORTED FILE TYPES
# ============================================================

SUPPORTED_EXTENSIONS = [
    ".db",
    ".sqlite",
    ".sqlite3",
    ".csv",
    ".xlsx",
    ".xls",
    ".json"
]


# ============================================================
# DATA LOADER
# ============================================================

class DataLoader:

    def __init__(self):

        self.file_path = None

        self.connection = None

        self.dataframes = {}

        self.file_type = None


    # ========================================================
    # LOAD FILE
    # ========================================================

    def load_file(self, file_path):

        if not file_path:

            raise ValueError(
                "No file was selected."
            )


        if not os.path.exists(file_path):

            raise FileNotFoundError(
                "Selected file does not exist."
            )


        self.file_path = file_path

        extension = os.path.splitext(
            file_path
        )[1].lower()

        self.file_type = extension


        # ----------------------------------------------------
        # CHECK SUPPORTED EXTENSION
        # ----------------------------------------------------

        if extension not in SUPPORTED_EXTENSIONS:

            raise ValueError(
                f"Unsupported file type: {extension}"
            )


        # ----------------------------------------------------
        # CLEAR PREVIOUS DATA
        # ----------------------------------------------------

        self.dataframes.clear()


        # ====================================================
        # SQLITE DATABASE
        # ====================================================

        if extension in [
            ".db",
            ".sqlite",
            ".sqlite3"
        ]:

            return self.load_sqlite(
                file_path
            )


        # ====================================================
        # CSV
        # ====================================================

        elif extension == ".csv":

            return self.load_csv(
                file_path
            )


        # ====================================================
        # EXCEL
        # ====================================================

        elif extension in [
            ".xlsx",
            ".xls"
        ]:

            return self.load_excel(
                file_path
            )


        # ====================================================
        # JSON
        # ====================================================

        elif extension == ".json":

            return self.load_json(
                file_path
            )


    # ========================================================
    # LOAD SQLITE
    # ========================================================

    def load_sqlite(self, file_path):

        self.connection = sqlite3.connect(
            file_path
        )

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


        tables = [
            row[0]
            for row in cursor.fetchall()
        ]


        if not tables:

            raise ValueError(
                "The SQLite database does not contain any tables."
            )


        # ----------------------------------------------------
        # Load every table into DataFrame
        # ----------------------------------------------------

        for table in tables:

            try:

                df = pd.read_sql_query(
                    f'SELECT * FROM "{table}"',
                    self.connection
                )

                self.dataframes[
                    table
                ] = df

            except Exception as error:

                print(
                    f"Could not load table {table}: {error}"
                )


        return {
            "type": "sqlite",
            "tables": tables,
            "connection": self.connection,
            "dataframes": self.dataframes
        }


    # ========================================================
    # LOAD CSV
    # ========================================================

    def load_csv(self, file_path):

        df = pd.read_csv(
            file_path
        )


        table_name = self.clean_table_name(
            os.path.basename(file_path)
        )


        self.dataframes[
            table_name
        ] = df


        # Create in-memory SQLite database

        self.create_memory_database()


        self.dataframes_to_sqlite()


        return {
            "type": "csv",
            "tables": [
                table_name
            ],
            "connection": self.connection,
            "dataframes": self.dataframes
        }


    # ========================================================
    # LOAD EXCEL
    # ========================================================

    def load_excel(self, file_path):

        sheets = pd.read_excel(
            file_path,
            sheet_name=None
        )


        for sheet_name, df in sheets.items():

            table_name = self.clean_table_name(
                sheet_name
            )


            # Avoid empty sheets

            if df is not None and not df.empty:

                self.dataframes[
                    table_name
                ] = df


        if not self.dataframes:

            raise ValueError(
                "The Excel file does not contain usable data."
            )


        # Create in-memory database

        self.create_memory_database()


        self.dataframes_to_sqlite()


        return {
            "type": "excel",
            "tables": list(
                self.dataframes.keys()
            ),
            "connection": self.connection,
            "dataframes": self.dataframes
        }


    # ========================================================
    # LOAD JSON
    # ========================================================

    def load_json(self, file_path):

        try:

            data = pd.read_json(
                file_path
            )

            table_name = self.clean_table_name(
                os.path.basename(file_path)
            )

            self.dataframes[
                table_name
            ] = data


        except Exception:

            # Try JSON records/list format

            import json

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)


            if isinstance(data, list):

                df = pd.DataFrame(
                    data
                )

            elif isinstance(data, dict):

                # Handle dictionary containing records

                df = pd.DataFrame(
                    data
                )

            else:

                raise ValueError(
                    "Unsupported JSON structure."
                )


            table_name = self.clean_table_name(
                os.path.basename(file_path)
            )


            self.dataframes[
                table_name
            ] = df


        if self.dataframes[table_name].empty:

            raise ValueError(
                "The JSON file contains no usable data."
            )


        # Create in-memory database

        self.create_memory_database()


        self.dataframes_to_sqlite()


        return {
            "type": "json",
            "tables": [
                table_name
            ],
            "connection": self.connection,
            "dataframes": self.dataframes
        }


    # ========================================================
    # CREATE MEMORY DATABASE
    # ========================================================

    def create_memory_database(self):

        # Close previous connection

        if self.connection:

            try:

                self.connection.close()

            except Exception:

                pass


        self.connection = sqlite3.connect(
            ":memory:"
        )


    # ========================================================
    # DATAFRAME → SQLITE
    # ========================================================

    def dataframes_to_sqlite(self):

        if not self.connection:

            self.create_memory_database()


        for table_name, df in self.dataframes.items():

            # Clean column names

            df = df.copy()

            df.columns = [
                self.clean_column_name(
                    column
                )
                for column in df.columns
            ]


            # Replace original dataframe

            self.dataframes[
                table_name
            ] = df


            # Write to SQLite

            df.to_sql(
                table_name,
                self.connection,
                if_exists="replace",
                index=False
            )


        self.connection.commit()


    # ========================================================
    # GET TABLES
    # ========================================================

    def get_tables(self):

        if not self.connection:

            return []


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


        return [
            row[0]
            for row in cursor.fetchall()
        ]


    # ========================================================
    # GET COLUMNS
    # ========================================================

    def get_columns(self, table_name):

        if not self.connection:

            return []


        cursor = self.connection.cursor()


        cursor.execute(
            f'PRAGMA table_info("{table_name}")'
        )


        return [
            row[1]
            for row in cursor.fetchall()
        ]


    # ========================================================
    # GET DATA
    # ========================================================

    def get_data(
        self,
        table_name,
        limit=None
    ):

        if not self.connection:

            return pd.DataFrame()


        query = f'SELECT * FROM "{table_name}"'


        if limit:

            query += f" LIMIT {int(limit)}"


        return pd.read_sql_query(
            query,
            self.connection
        )


    # ========================================================
    # EXECUTE SQL
    # ========================================================

    def execute_query(
        self,
        query
    ):

        if not self.connection:

            raise ValueError(
                "No database has been loaded."
            )


        cursor = self.connection.cursor()


        cursor.execute(
            query
        )


        # ----------------------------------------------------
        # SELECT / result query
        # ----------------------------------------------------

        if cursor.description:

            columns = [
                description[0]
                for description in cursor.description
            ]


            rows = cursor.fetchall()


            return {
                "columns": columns,
                "rows": rows
            }


        # ----------------------------------------------------
        # INSERT / UPDATE / DELETE etc.
        # ----------------------------------------------------

        self.connection.commit()


        return {
            "columns": [],
            "rows": [],
            "affected_rows": cursor.rowcount
        }


    # ========================================================
    # GET DATABASE SCHEMA
    # ========================================================

    def get_schema(self):

        schema = {}


        for table in self.get_tables():

            schema[
                table
            ] = self.get_columns(
                table
            )


        return schema


    # ========================================================
    # CLEAN TABLE NAME
    # ========================================================

    def clean_table_name(
        self,
        name
    ):

        name = os.path.splitext(
            name
        )[0]


        name = name.strip()


        # Replace spaces and symbols

        cleaned = ""

        for char in name:

            if char.isalnum() or char == "_":

                cleaned += char

            else:

                cleaned += "_"


        if not cleaned:

            cleaned = "data"


        if cleaned[0].isdigit():

            cleaned = "table_" + cleaned


        return cleaned


    # ========================================================
    # CLEAN COLUMN NAME
    # ========================================================

    def clean_column_name(
        self,
        name
    ):

        name = str(
            name
        ).strip()


        cleaned = ""

        for char in name:

            if char.isalnum() or char == "_":

                cleaned += char

            else:

                cleaned += "_"


        if not cleaned:

            cleaned = "column"


        if cleaned[0].isdigit():

            cleaned = "column_" + cleaned


        return cleaned


    # ========================================================
    # CLOSE
    # ========================================================

    def close(self):

        if self.connection:

            try:

                self.connection.close()

            except Exception:

                pass

            self.connection = None