CREATE VIEW genre_by_year AS (
    SELECT
        ar.year AS year,
        COUNT(*) AS num_genres
    FROM artist_rank ar
    NATURAL JOIN artist_genre ag
    GROUP BY
        year
    ORDER BY 
        year
)
;

CREATE VIEW genre_by_city AS (
    SELECT
        ac.city_id AS city_id,
        COUNT(*) AS num_genres
    FROM artist_city ac
    NATURAL JOIN artist_genre ag
    GROUP BY
        city_id
    ORDER BY 
        city_id
)
;