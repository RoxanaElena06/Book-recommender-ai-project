import anthropic
from schema_context import SCHEMA_CONTEXT

import os
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def extract_text(response) -> str:
    text_blocks = [block.text for block in response.content if block.type == "text"]
    return "".join(text_blocks).strip()


def clean_sql(raw_sql: str) -> str:
    # Sometimes the model wraps its answer in a markdown code fence
    # (```sql ... ```) even when told not to. Strip that off before
    # the query is validated or executed.
    cleaned = raw_sql.strip()
    if cleaned.startswith("```"):
        # Remove the opening fence (handles ```sql or plain ```)
        cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned
        cleaned = cleaned.lstrip("sql").lstrip()  # in case "sql" stuck to the fence
    if cleaned.endswith("```"):
        cleaned = cleaned.rsplit("```", 1)[0]
    return cleaned.strip()


def question_to_sql(user_question: str) -> str:
    prompt = f"""You are a SQL generator for a Spark SQL / Databricks environment.
Here is the schema you must use:

{SCHEMA_CONTEXT}

Generate ONLY a valid SQL SELECT query (no explanation, no markdown formatting,
just the raw SQL) that answers this question:

{user_question}
"""
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    raw_output = extract_text(response)
    return clean_sql(raw_output)


if __name__ == "__main__":
    from execute_sql import execute_query

    question = "Which genre has the highest average rating with at least 1000 books?"
    sql_query = question_to_sql(question)
    print("Generated SQL:\n", sql_query)

    columns, rows = execute_query(sql_query)
    print("\nColumns:", columns)
    print("Results:")
    for row in rows:
        print(row)


def phrase_answer(question: str, columns, rows) -> str:
    # Turn the raw result rows into a simple text block so Claude can read it
    result_text = str(columns) + "\n" + "\n".join(str(r) for r in rows[:20])

    prompt = f"""A user asked this question about a book dataset: "{question}"

Here are the query results:
{result_text}

Write a short, clear, one-to-two sentence answer to their question based
only on this data. Do not make up any numbers not shown above."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip()