SELECT 
    ag.genre, 
    COUNT(*)/(SELECT num_genres FROM genre_by_city WHERE city_id = {city_id}) AS percent
FROM artist_city ac
NATURAL JOIN artist_genre ag
WHERE city_id = {city_id}
GROUP BY
    genre
ORDER BY 
    percent DESC
LIMIT 10
;