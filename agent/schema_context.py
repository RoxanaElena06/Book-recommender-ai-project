# This is just a plain text description of your data model, written by hand.
# It's what tells Claude what tables/columns exist, so it can generate
# accurate SQL. This is NOT your actual data — just its shape/structure.

SCHEMA_CONTEXT = """
Table: dim_books
Columns:
  book_id (int, primary key)
  title (string)
  authors (array of strings)
  genres (array of strings)
  original_publication_year (int)
  pages (int)
  average_rating (float)
  ratings_count (int)
  popularity_bucket (int, 1-4, 4 = most rated)

Table: fact_ratings
Columns:
  user_id (int)
  book_id (int, foreign key to dim_books.book_id)
  rating (int, 1-5)

Sample dim_books row:
  book_id=1, title="The Hunger Games", authors=["Suzanne Collins"],
  genres=["young-adult","fiction","fantasy"], original_publication_year=2008,
  pages=374, average_rating=4.34, ratings_count=4780653, popularity_bucket=4
"""