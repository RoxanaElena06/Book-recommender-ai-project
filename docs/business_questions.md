# Business Questions

- **Which genres have the highest average rating vs. highest volume of ratings?**

**A:** science, historical-fiction, contemporary
```sql
select genre, round(avg(average_rating)) as avg_rating, count(*) as num_books
from workspace.default.dim_books lateral view explode(genres) as genre
group by genre 
order by avg_rating desc
limit 15;
```

- **Which authors are most "polarizing" (highest rating variance, min N ratings)?**

**A:** Haruki Murakami, Nicholas Sparks, Laurell K. Hamilton, L.J. Smith and Tamora Pierce
```sql
select author, round(stddev(f.rating), 2) as rating_stddev, count(*) as num_books
from workspace.default.fact_ratings f join workspace.default.dim_books d on f.book_id = d.book_id
lateral view explode(d.authors) as author
group by author
having count(*) >= 20
order by rating_stddev desc
limit 15;
```
- **Does page count correlate with rating?**

**A:** Result (0.12430523325041243) is close to 0, is more like a no relationship between page and ratig. Page count doesn't predict rating 
```sql
select count(*) as num_books, corr(pages, average_rating) as page_rating_corr
from workspace.default.dim_books
where pages is not null and average_rating is not null;
```
- **How does the ratings distribution trend by publication year?**

**A:** The number of books per publication year grows steadily from the early 1900s through the 2010s, peaking around ~560 books in the most-represented year.
```sql
select original_publication_year, round(avg(average_rating)) as avg_rating, count(*) as num_books, SUM(ratings_count) AS total_ratings
from workspace.default.dim_books
where original_publication_year is not null and original_publication_year between 1900 and 2020
group by original_publication_year
order by original_publication_year asc;
```
- **Which books are most "underrated" (high rating, low ratings_count)?**

**A:** ESV Study Bible, Mark of the Lion Trilogy, Attack of the Deranged Mutant Killer Monster Snow Goons, Preach My Gospel: A Guide To Missionary Service and The Way of Kings, Part 1 (The Stormlight Archive #1.1)
```sql
select title, average_rating, ratings_count
from workspace.default.dim_books
where average_rating >= 4.2
  and ratings_count < 10000
  and ratings_count > 100
order by  average_rating desc, ratings_count asc
limit 15;
```