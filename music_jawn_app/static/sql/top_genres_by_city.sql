SELECT 
    genre, 
    COUNT(*)/(
        SELECT 
            COUNT(*) 
        FROM (SELECT * FROM artist_city NATURAL JOIN artist_genre WHERE city_id = {city_id}) t1
    ) AS percent
FROM
    (SELECT * FROM artist_city NATURAL JOIN artist_genre WHERE city_id = {city_id}) t2
GROUP BY 
    genre
ORDER BY 
    percent DESC
LIMIT 10
;