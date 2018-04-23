SELECT 
    genre, 
    COUNT(*)/(
        SELECT 
            COUNT(*) 
        FROM (SELECT * FROM artist_rank NATURAL JOIN artist_genre WHERE year = {year}) t1
    ) AS percent
FROM
    (SELECT * FROM artist_rank NATURAL JOIN artist_genre WHERE year = {year}) t2
GROUP BY 
    genre
ORDER BY 
    percent DESC
LIMIT 10
;