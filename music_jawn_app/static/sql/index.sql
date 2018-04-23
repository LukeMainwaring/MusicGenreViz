CREATE INDEX part_of_artist_id ON artist_genre (artist_id(10));

CREATE INDEX city_idx ON artist_city (city_id);

CREATE INDEX year_idx ON artist_rank (year);
