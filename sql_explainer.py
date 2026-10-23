# ============================================================
# SQL EXPLAINER
# ============================================================

import os
from openai import OpenAI


class SQLExplainer:

    def __init__(self):

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
    # EXPLAIN SQL
    # ========================================================

    def explain_sql(self, sql):

        if not sql.strip():

            return "No SQL query was provided."


        prompt = f"""
You are an expert SQL teacher.

Explain the following SQLite SQL query
in simple language.

SQL QUERY:

{sql}


Give the explanation in this format:

PURPOSE:
Explain what the query is trying to accomplish.

STEP-BY-STEP:
Explain each important part of the query.

TABLES USED:
List the tables used.

COLUMNS USED:
List the important columns used.

FILTERS:
Explain WHERE conditions if present.

JOINS:
Explain JOIN conditions if present.

GROUPING:
Explain GROUP BY if present.

SORTING:
Explain ORDER BY if present.

LIMIT:
Explain LIMIT if present.

DATABASE CHANGES:
If the query changes the database, clearly explain
what it changes.

SAFETY:
Explain whether the query is read-only or modifies
database data/structure.

IMPORTANT:

- Use simple English.
- Do not change the SQL.
- Do not generate a different SQL query.
- Explain the provided SQL only.
"""


        try:

            response = self.client.responses.create(

                model="gpt-5-mini",

                input=prompt
            )


            explanation = response.output_text.strip()

            return explanation


        except Exception as error:

            return (
                "Unable to explain SQL.\n\n"
                f"Error: {error}"
            )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("Testing SQL Explainer...")


    try:

        explainer = SQLExplainer()


        sql = """
        SELECT
            c.name,
            SUM(o.amount) AS total_spending
        FROM customers c
        JOIN orders o
            ON c.id = o.customer_id
        GROUP BY c.id, c.name
        ORDER BY total_spending DESC
        LIMIT 10;
        """


        result = explainer.explain_sql(
            sql
        )


        print("\nSQL:")
        print("-" * 60)
        print(sql)


        print("\nEXPLANATION:")
        print("-" * 60)
        print(result)


    except Exception as error:

        print("\nERROR:")
        print(error)