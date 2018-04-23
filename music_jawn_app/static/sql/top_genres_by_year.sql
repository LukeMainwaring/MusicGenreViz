SELECT 
    ag.genre, 
    COUNT(*)/(SELECT num_genres FROM genre_by_year WHERE year = {year}) AS percent
FROM artist_rank ar
NATURAL JOIN artist_genre ag
WHERE year = {year}
GROUP BY
    genre
ORDER BY 
    percent DESC
LIMIT 10