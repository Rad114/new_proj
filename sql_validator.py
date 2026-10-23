# ============================================================
# SQL VALIDATOR
# ============================================================


class SQLValidator:

    def __init__(self):
        pass


    # ========================================================
    # VALIDATE SQL
    # ========================================================

    def validate(self, sql):

        if not sql:

            return {
                "valid": False,
                "type": "UNKNOWN",
                "dangerous": False,
                "message": "SQL query is empty."
            }


        sql = sql.strip()


        if not sql:

            return {
                "valid": False,
                "type": "UNKNOWN",
                "dangerous": False,
                "message": "SQL query is empty."
            }


        sql_type = self.detect_type(
            sql
        )


        dangerous = self.is_dangerous(
            sql
        )


        return {
            "valid": True,
            "type": sql_type,
            "dangerous": dangerous,
            "message": self.get_message(
                sql_type,
                dangerous
            )
        }


    # ========================================================
    # DETECT SQL TYPE
    # ========================================================

    def detect_type(self, sql):

        text = sql.strip().upper()


        # SELECT

        if text.startswith("SELECT"):

            return "SELECT"


        # WITH / CTE

        if text.startswith("WITH"):

            return "WITH / CTE"


        # INSERT

        if text.startswith("INSERT"):

            return "INSERT"


        # UPDATE

        if text.startswith("UPDATE"):

            return "UPDATE"


        # DELETE

        if text.startswith("DELETE"):

            return "DELETE"


        # CREATE TRIGGER

        if text.startswith("CREATE TRIGGER"):

            return "CREATE TRIGGER"


        # DROP TRIGGER

        if text.startswith("DROP TRIGGER"):

            return "DROP TRIGGER"


        # CREATE TABLE

        if text.startswith("CREATE TABLE"):

            return "CREATE TABLE"


        # DROP TABLE

        if text.startswith("DROP TABLE"):

            return "DROP TABLE"


        # ALTER TABLE

        if text.startswith("ALTER TABLE"):

            return "ALTER TABLE"


        # CREATE VIEW

        if text.startswith("CREATE VIEW"):

            return "CREATE VIEW"


        # DROP VIEW

        if text.startswith("DROP VIEW"):

            return "DROP VIEW"


        # CREATE INDEX

        if (
            text.startswith("CREATE INDEX")
            or
            text.startswith("CREATE UNIQUE INDEX")
        ):

            return "CREATE INDEX"


        # DROP INDEX

        if text.startswith("DROP INDEX"):

            return "DROP INDEX"


        # PRAGMA

        if text.startswith("PRAGMA"):

            return "PRAGMA"


        # BEGIN

        if text.startswith("BEGIN"):

            return "BEGIN TRANSACTION"


        # COMMIT

        if text.startswith("COMMIT"):

            return "COMMIT"


        # ROLLBACK

        if text.startswith("ROLLBACK"):

            return "ROLLBACK"


        return "UNKNOWN"


    # ========================================================
    # CHECK DANGEROUS OPERATIONS
    # ========================================================

    def is_dangerous(self, sql):

        text = sql.upper()


        dangerous_commands = [

            "DROP TABLE",

            "DROP VIEW",

            "DROP TRIGGER",

            "DROP INDEX",

            "DELETE FROM",

            "UPDATE ",

            "ALTER TABLE",

            "VACUUM",

            "DETACH DATABASE"
        ]


        for command in dangerous_commands:

            if command in text:

                return True


        return False


    # ========================================================
    # MESSAGE
    # ========================================================

    def get_message(
        self,
        sql_type,
        dangerous
    ):

        if dangerous:

            return (
                f"{sql_type} detected.\n\n"
                "This operation can change or remove "
                "data/database objects.\n\n"
                "Confirmation is required."
            )


        if sql_type == "SELECT":

            return (
                "SELECT query detected.\n\n"
                "This is a read-only operation."
            )


        if sql_type == "INSERT":

            return (
                "INSERT query detected.\n\n"
                "This will add data to the database."
            )


        if sql_type == "CREATE TRIGGER":

            return (
                "CREATE TRIGGER detected.\n\n"
                "This will create a database trigger."
            )


        if sql_type == "CREATE TABLE":

            return (
                "CREATE TABLE detected.\n\n"
                "This will create a new table."
            )


        if sql_type == "CREATE VIEW":

            return (
                "CREATE VIEW detected.\n\n"
                "This will create a database view."
            )


        if sql_type == "CREATE INDEX":

            return (
                "CREATE INDEX detected.\n\n"
                "This will create a database index."
            )


        return (
            f"{sql_type} query detected."
        )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    validator = SQLValidator()


    queries = [

        "SELECT * FROM customers;",

        "INSERT INTO customers "
        "(name) VALUES ('John');",

        "UPDATE customers "
        "SET name='John' "
        "WHERE id=1;",

        "DELETE FROM customers "
        "WHERE id=1;",

        """
        CREATE TRIGGER update_time
        AFTER UPDATE ON customers
        FOR EACH ROW
        BEGIN
            UPDATE customers
            SET name = NEW.name
            WHERE id = NEW.id;
        END;
        """,

        "DROP TABLE customers;"
    ]


    for query in queries:

        result = validator.validate(
            query
        )


        print("=" * 60)

        print("SQL:")

        print(query)

        print("\nType:")

        print(
            result["type"]
        )

        print("\nDangerous:")

        print(
            result["dangerous"]
        )

        print("\nMessage:")

        print(
            result["message"]
        )