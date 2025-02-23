DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
    id SERIAL,
    title TEXT,
    contents TEXT
);
INSERT INTO posts (title, contents)
VALUES ('test', 'cool stuff'),
    ('test2', 'cool stuff2');