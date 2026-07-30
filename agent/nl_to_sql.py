import anthropic
from schema_context import SCHEMA_CONTEXT

# NEVER hardcode your API key directly in code that goes on GitHub.
# Store it as an environment variable instead, and read it like this:
import os
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def extract_text(response) -> str:
    # response.content can include multiple block types (thinking, text, tool_use, etc).
    # Instead of assuming position, we specifically look for the text block(s)
    # and join them — this works regardless of how many/which other block
    # types the model includes.
    text_blocks = [block.text for block in response.content if block.type == "text"]
    return "".join(text_blocks).strip()


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
    return extract_text(response)


if __name__ == "__main__":
    # Quick manual test
    sql = question_to_sql("Which genre has the highest average rating with at least 1000 books?")
    print(sql)