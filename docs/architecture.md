# Architecture
**To be fill in on Day 17.** 
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