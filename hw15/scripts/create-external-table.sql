use raw;

DROP TABLE IF EXISTS game_sales;

CREATE EXTERNAL TABLE IF NOT EXISTS game_sales 
(
    name STRING,
    platform STRING,
    release_year INT,
    genre STRING,
    publisher STRING,
    na_sales FLOAT,
    eu_sales FLOAT,
    jp_sales FLOAT,
    other_sales FLOAT,
    global_sales FLOAT,
    critic_score FLOAT,
    critic_count INT,
    user_score FLOAT,
    user_count INT,
    developer STRING,
    rating STRING
)
COMMENT 'Create external table `game_sales` in `raw` database'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LOCATION '/tmp/hive/data/'
TBLPROPERTIES ("skip.header.line.count"="1");
