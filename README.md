# Book Data Platform — DA/DE Portfolio Project
An end-to-end data pipeline and analytics platform built on the Goodbooks-10k dataset (~10,000 books, 6 million ratings) — covering ETL, data modeling, orchestration, multi-tool dashboards, and a natural-language-to-SQL agent.

## Business questions answered
- Which genres have the highest average rating vs. highest volume?
- Which authors are most "polarizing" (highest rating variance)?
- Does page count correlate with rating?
- How does the ratings distribution trend by publication year?
- Which books are most "underrated"?

See full queries and findings: [docs/business_answers.sql](docs/business_answers.sql)

## Architecture
![Architecture diagram](docs/dashboard_export.png)

## Book agent
https://book-recommender-ai-project-f7dqe74r9igmyxntpe38kg.streamlit.app/ 

## What each component does
**`01_etl_clean_books.ipynb`** 
- reads raw CSVs from S3, cleans and validates them (schema checks, null/duplicate quality gates, tested failure paths), writes idempotent Delta tables via MERGE INTO.
**`02_data_modeling.ipynb`** 
-  builds a star schema (`dim_books`,`fact_ratings`) from the cleaned tables, answers the business questions above in SQL.
**`bonus_content_similarity.ipynb`** 
- a secondary content-based book recommender (TF-IDF + cosine similarity), reading from `dim_books`.
**`agent/`** 
- a natural-language-to-SQL assistant: translates plain English questions into validated, guardrailed SQL against the star schema, executes it, and phrases a plain-English answer. Deployed live at [your Streamlit URL here].
**Orchestration** 
- a scheduled Databricks Job (`book_pipeline_job`) chains the ETL and modeling notebooks, with retries and failure email alerts (tested by inducing a deliberate failure).
**Dashboards** 
- the same findings visualized across Databricks Lakeview, Power BI, and Tableau Public, each connected live to the Databricks warehouse. See `docs/` for exports and links.
**`docs/`**
- architecture notes, tested-proof of reliability (quality gate tests, idempotency tests, failure alerting test), and dashboard exports.

## How to run it
1. Clone this repo
2. Notebooks (`01_etl_clean_books`, `02_data_modeling`) are designed to run in a Databricks workspace with a Volume containing the raw goodbooks-10k CSVs at `/Volumes/workspace/default/books_raw/`
3. For the agent: `cd agent`, `pip install -r ../requirements.txt`, set `ANTHROPIC_API_KEY` and Databricks connection env vars (or `.env`), then `streamlit run app.py`
4. Or just try the live deployed version: [your Streamlit URL]

## What I'd improve with more time
- Real SQL parsing for the agent's guardrails instead of a keyword check
- Automated tests (currently manual quality-gate testing, documented in `docs/architecture.md`)
- CI pipeline to run tests on every push
- Composite-key idempotent merge for `fact_ratings` (currently a simpler overwrite)
	

