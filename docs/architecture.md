# Architecture
To planned flow: S3 (raw) -> Databricks ETL (PySpark/Delta) -> data modeling (star schema)

## ETL reliability — Day 3 quality gate tests
**Test 1 — null key values (books table):**
Injected 2 null `book_id` values into a 20-row sample of the books data, keeping ratings and book_tags unmodified. Ran the full ETL notebook against this corrupted folder. 
Result: the pipeline correctly raised a `ValueError` at the `quality_gate()` step and halted before any data was written to Delta tables — confirmed no partial/bad writes occurred downstream.

## ETL reliability — Day 4 idempotency merge test
Ran the full ETL notebook twice consecutively against the real dataset.
- Books table row count after run 1: 10000
- Books table row count after run 2: 5976479 (identical — confirms no duplication)
- Ratings table row count after run 1: 10000
- Ratings table row count after run 2: 5976479 (identical)

Books and ratings now use Delta Lake MERGE INTO (upsert) instead of full overwrite, matching real incremental-load patterns. book_tags remains a full overwrite by design, since it's a small, fully-rebuilt reference table.

## Star schema design (Day 5)

### dim_books (grain: one row per book)
   | Target column | Source | Notes |
   |---|---|---|
   | book_id | books.book_id | primary key |
   | title | books.title | |
   | authors | books.authors | stored as a string like "['Author Name']" — needs cleanup |
   | genres | books.genres | stored as a string like "['genre1','genre2']" — needs parsing into an array |
   | original_publication_year | books.original_publication_year | cast to int |
   | pages | books.pages | cast to int |
   | average_rating | books.average_rating | |
   | ratings_count | books.ratings_count | |
   
### fact_ratings (grain: one row per user-book rating)
   | Target column | Source | Notes |
   |---|---|---|
   | user_id | ratings.user_id | |
   | book_id | ratings.book_id | foreign key to dim_books.book_id |
   | rating | ratings.rating | |

## Orchestration — Day 10–11
### Job configuration
The pipeline runs as a single Databricks Job, `book_pipeline_job`, with a three-task dependency chain:
1. `run_etl` - runs `01_etl_clean_books`, reads raw CSVs, writes `books`/`ratings`/`book_tags` Delta tables.
2. `run_data_modeling` - depends on `run_etl` succeeding and runs `02_data_modeling`, builds the `dim_books`/`fact_ratings` star schema.
3. `run_commender` - depends on `run_data_modeling` succeeding.

Compute: Serverless (no manually managed cluster).

### Schedule
Runs daily at 8:00 AM

### Reliability configuration
- Retries: 1 minute delay, up to 3 attempts per task (4 total attempts)
- Failure notifications: email alert sent on failure to genesroxanaelena@gmail.com

### Failure test
1. To verify the alerting actually works, the `run_etl` task's `raw_volume_path` parameter was temporarily set to a non-existent path (`/Volumes/workspace/default/books_raw/does_not_exist/`) and the Job was triggered manually.
2. Result: `run_etl` failed as expected, `run_data_modeling` and `run_commender` correctly did not execute  and a failure email notification was received.
