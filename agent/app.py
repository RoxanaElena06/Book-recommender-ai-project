import os
import streamlit as st

# ── Bridge secrets FIRST, before importing anything that needs them
from dotenv import load_dotenv
load_dotenv()  # for local development via .env

try:
    for key in ["ANTHROPIC_API_KEY", "DATABRICKS_HOST", "DATABRICKS_HTTP_PATH", "DATABRICKS_TOKEN"]:
        if key in st.secrets:
            os.environ[key] = st.secrets[key]
except Exception:
    pass  # no secrets.toml locally — expected, .env already loaded above

# ── NOW it's safe to import your own modules, since the environment
# variables they need are already set

from nl_to_sql import question_to_sql, phrase_answer
from execute_sql import execute_query, get_table_preview


# ── Page setup 
st.set_page_config(
    page_title="Book Data Assistant",
    page_icon="📚",
    layout="centered"
)

# ── Basic custom styling
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    .subtitle {
        color: #9aa0a6;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .example-questions {
        color: #9aa0a6;
        font-size: 0.9rem;
    }
    .section-header {
        margin-top: 2.5rem;
        border-top: 1px solid #262730;
        padding-top: 1.5rem;
    }
    .footer-note {
        color: #6b7280;
        font-size: 0.8rem;
        margin-top: 3rem;
        border-top: 1px solid #262730;
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Header / intro 
st.title("📚 Book Data Assistant")
st.markdown(
    '<p class="subtitle">Ask a question about the book dataset in plain English.</p>',
    unsafe_allow_html=True
)

# ── Example questions 
st.markdown('<p class="example-questions">Try one of these, or ask your own:</p>', unsafe_allow_html=True)

example_questions = [
    "Which genre has the highest average rating with at least 1000 books?",
    "Which authors are most polarizing among readers?",
    "What is the total number of books in the database?",
    "Which books are the most underrated?",
]

if "question_input" not in st.session_state:
    st.session_state.question_input = ""

cols = st.columns(2)
for i, eq in enumerate(example_questions):
    if cols[i % 2].button(eq, use_container_width=True):
        st.session_state.question_input = eq

st.markdown("---")

# ── Question input 
question = st.text_input(
    "Ask questions:",
    value=st.session_state.question_input,
    placeholder="e.g. Which genre has the highest average rating?"
)

# ── Run the pipeline 
if question:
    with st.spinner("Translating your question into SQL..."):
        sql_query = question_to_sql(question)

    st.subheader("Generated SQL")
    st.code(sql_query, language="sql")

    with st.spinner("Running the query against the book database..."):
        columns, rows = execute_query(sql_query)

    with st.spinner("Writing your answer..."):
        answer = phrase_answer(question, columns, rows)

    st.subheader("Answer")
    st.success(answer)

# ── Dataset description + preview (shown below the question section) ─
st.markdown('<div class="section-header"></div>', unsafe_allow_html=True)
st.subheader("About this dataset")
st.markdown("""
This assistant is built on the **Goodbooks-10k** dataset — roughly 10,000
books and 6 million reader ratings, originally sourced from Goodreads.

**Files behind this project:**
- `books_enriched.csv` — book metadata (title, authors, genres, page count, publication year, average rating)
- `ratings.csv` — ~6 million individual user ratings (1–5 stars)
- `book_tags.csv` — reader-applied tags per book

The raw data was cleaned and loaded through a PySpark/Delta Lake pipeline
on Databricks, then modeled into a star schema (`dim_books`, `fact_ratings`)
before being made queryable through this assistant.
""")

with st.spinner("Loading a preview of the data..."):
    try:
        columns, rows = get_table_preview("dim_books", limit=5)
        st.dataframe(
            {col: [row[i] for row in rows] for i, col in enumerate(columns)},
            use_container_width=True
        )
    except Exception as e:
        st.caption(f"Preview unavailable right now: {e}")

# ── Footer 
st.markdown(
    '<p class="footer-note">Built as a portfolio project: AWS S3 → Databricks '
    '(PySpark, Delta Lake) → star-schema data model → Claude API for '
    'natural-language-to-SQL. Only SELECT queries are permitted; all generated '
    'SQL is validated before execution.</p>',
    unsafe_allow_html=True
)