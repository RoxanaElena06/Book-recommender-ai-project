# An end-to-end data pipeline and analytics platform for book data built on the goodbooks-10k dataset
— ETL, orchestration, natural-language query agent
— PySpark
— Delta Lake
— Scikit-learn

## Progress 
- Sprint 0: AWS S3 setup, dataset uploaded 
- Sprint 1: ETL pipeline in Databricks (PySpark + Delta Lake):
	- books, ratings and book_tags tables built and cleaned 
	- GitHub cleanup: consolidated 5 old practice repos into one organized Data-analyst-practice-GeeksforGeeks repository
	- Databricks Free Edition notebook - read and clean the csv's files using PySpark (cleaned result as a Delta Lake table)
	- Using Scikit-learn, build a TF-IDF representation of each book's genres, compute cosine similarity, recommend "books like this one."
	

