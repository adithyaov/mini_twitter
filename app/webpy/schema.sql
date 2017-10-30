CREATE TABLE Users(id INT, name TEXT, password TEXT, email TEXT);
CREATE TABLE Tweets(id INT, title TEXT, content TEXT, user_id INT);
CREATE TABLE Following(id INT, user_id INT, following_ids TEXT);