DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  quizname  TEXT NOT NULL,
  FOREIGN KEY (username) REFERENCES user (username)
);

CREATE TABLE quiz (
  username TEXT NOT NULL,
  quizname TEXT NOT NULL,
  ques TEXT NOT NULL,
  options TEXT NOT NULL,
  FOREIGN KEY (username) REFERENCES user(username),
  FOREIGN KEY (quizname) REFERENCES post (quizname)
);

CREATE TABLE quiz_answers (
  username TEXT NOT NULL,
  quizname TEXT NOT NULL,
  ques TEXT NOT NULL,
  ans TEXT NOT NULL,
  FOREIGN KEY (username) REFERENCES user(username)
)
