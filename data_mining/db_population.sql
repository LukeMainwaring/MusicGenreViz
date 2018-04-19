CREATE TABLE IF NOT EXISTS artist (
    artist_id         VARCHAR(25) NOT NULL,
    artist_name       VARCHAR(50) NOT NULL,
    artist_sp_name    VARCHAR(50) NOT NULL,
    PRIMARY KEY (artist_id)
);

CREATE TABLE IF NOT EXISTS artist_genre (
    artist_id         VARCHAR(25) NOT NULL,
    genre             VARCHAR(50) NOT NULL,
    PRIMARY KEY(artist_id, genre),
    FOREIGN KEY(artist_id) references artist(artist_id)
);

CREATE TABLE IF NOT EXISTS city (
    city_id           INT         NOT NULL AUTO_INCREMENT,
    city_name         VARCHAR(50) NOT NULL,
    city_state        VARCHAR(50) NOT NULL,
    city_lat          FLOAT       NOT NULL,
    city_lon          FLOAT       NOT NULL,
    PRIMARY KEY (city_id)
);

CREATE TABLE IF NOT EXISTS artist_city (
    artist_id         VARCHAR(25) NOT NULL,
    city_id           INT         NOT NULL,
    arr_index         INT         NOT NULL,
    PRIMARY KEY(artist_id, city_id, arr_index),
    FOREIGN KEY(artist_id) references artist(artist_id),
    FOREIGN KEY(city_id) references city(city_id)
);

CREATE TABLE IF NOT EXISTS artist_rank (
    artist_id         VARCHAR(25) NOT NULL,
    year              INT         NOT NULL,
    a_rank            INT         NOT NULL,
    PRIMARY KEY (artist_id, year, a_rank),
    FOREIGN KEY(artist_id) references artist(artist_id)
);


