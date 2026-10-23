# ============================================================
# AI SQL GENERATOR
# ============================================================

import os
from openai import OpenAI


class SQLGenerator:

    def __init__(self):

        # Get API key from Windows environment variable
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OpenAI API key not found.\n\n"
                "Please set OPENAI_API_KEY first."
            )

        self.client = OpenAI(
            api_key=api_key
        )


    # ========================================================
    # GENERATE SQL
    # ========================================================

    def generate_sql(self, question, schema):

        if not question.strip():

            return "-- Please enter a question."


        if not schema.strip():

            return "-- No database schema found."


        prompt = f"""
You are an expert SQLite SQL developer.

Convert the user's natural-language request into
valid SQLite SQL.

DATABASE SCHEMA:
{schema}

USER REQUEST:
{question}


You can generate all valid SQLite SQL operations,
including:

1. SELECT
2. INSERT
3. UPDATE
4. DELETE

5. CREATE TABLE
6. ALTER TABLE
7. DROP TABLE

8. CREATE VIEW
9. DROP VIEW

10. CREATE INDEX
11. DROP INDEX

12. CREATE TRIGGER
13. DROP TRIGGER

14. INNER JOIN
15. LEFT JOIN
16. CROSS JOIN

17. UNION
18. UNION ALL

19. WITH / CTE
20. Subqueries

21. GROUP BY
22. HAVING
23. ORDER BY
24. LIMIT

25. CASE
26. Aggregate functions
27. Window functions

28. BEGIN
29. COMMIT
30. ROLLBACK

31. PRAGMA

IMPORTANT RULES:

- Use SQLite syntax.
- Use only tables that exist in the schema.
- Use only columns that exist in the schema.
- Do not invent table names.
- Do not invent column names.
- Return ONLY SQL.
- Do not explain the SQL.
- Do not use markdown.
- Do not put the SQL inside ``` blocks.

If the request cannot be answered using the
provided schema, return exactly:

-- Unable to generate SQL from the provided schema.
"""


        try:

            response = self.client.responses.create(

                model="gpt-5-mini",

                input=prompt
            )


            sql = response.output_text.strip()


            # Remove markdown if AI accidentally returns it

            if sql.startswith("```sql"):

                sql = sql[6:]


            elif sql.startswith("```"):

                sql = sql[3:]


            if sql.endswith("```"):

                sql = sql[:-3]


            return sql.strip()


        except Exception as error:

            return (
                "-- ERROR WHILE GENERATING SQL\n"
                f"-- {error}"
            )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("Testing AI SQL Generator...")

    try:

        generator = SQLGenerator()


        schema = """
        TABLE customers
        (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT
        );

        TABLE orders
        (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            amount REAL,
            order_date TEXT
        );
        """


        question = (
            "Find the top 10 customers "
            "by total spending."
        )


        result = generator.generate_sql(
            question,
            schema
        )


        print("\nGenerated SQL:")
        print("-" * 60)
        print(result)
        print("-" * 60)


    except Exception as error:

        print("\nERROR:")
        print(error)