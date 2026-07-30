from databricks import sql
import os

def is_safe_select(query: str) -> bool:
    # only allow queries that start with SELECT
    normalized = query.strip().upper()
    forbidden_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE", ";"]
    if not normalized.startswith("SELECT"):
        return False
    if any(word in normalized for word in forbidden_keywords):
        return False
    return True

def add_row_limit(query: str, max_rows: int = 100) -> str:
    # Safety net: if the generated query doesn't already have a LIMIT, add one
    if "LIMIT" not in query.upper():
        query = query.rstrip(";") + f" LIMIT {max_rows}"
    return query

def execute_query(query: str):
    if not is_safe_select(query):
        raise ValueError(f"Rejected unsafe query: {query}")

    query = add_row_limit(query)

    with sql.connect(
        server_hostname=os.environ["DATABRICKS_HOST"],
        http_path=os.environ["DATABRICKS_HTTP_PATH"],
        access_token=os.environ["DATABRICKS_TOKEN"]
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return columns, rows