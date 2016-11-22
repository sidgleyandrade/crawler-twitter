CREATE TABLE IF NOT EXISTS %s.%s (
    id BIGINT NOT NULL,
    id_str TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    date DATE NULL,
    favorite_count INT,
    favorited BOOLEAN,
    lang TEXT NULL,
    retweet_count INT NULL,
    retweeted BOOLEAN NULL,
    text TEXT NULL,
    user_id BIGINT NULL,
    user_id_str TEXT NULL,
    user_name TEXT NULL,
    user_screen_name TEXT NULL,
    user_contributors_enabled BOOLEAN NULL,
    user_followers_count INT NULL,
    user_friends_count INT NULL,
    user_geo_enabled BOOLEAN NULL,
    user_lang TEXT NULL,
    user_location TEXT NULL,
    user_protected BOOLEAN NULL,
    user_time_zone TEXT NULL,
    user_utc_offset INT NULL,
    place_country TEXT NULL,
    place_country_code TEXT NULL,
    place_full_name TEXT NULL,
    place_name TEXT NULL,
    place_place_type TEXT NULL,
    tweet JSON,
    CONSTRAINT %s_pk PRIMARY KEY (id_str)
);

SELECT AddGeometryColumn ('%s','%s','coordinates', 4326, 'POINT', 2)
WHERE NOT EXISTS (SELECT column_name FROM information_schema.columns
		  WHERE	table_schema = '%s' AND
		        table_name ='%s' AND
			    column_name = 'coordinates');

CREATE INDEX IF NOT EXISTS date_%s_ix ON %s.%s (date);
