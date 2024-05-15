# Databse: mywebsite
## Table: members
| Colunm Name | Data Type | Additional Settings | Description |
| ----------- | --------- | ------------------- | ----------- |
| id | bigint | primary key, auto increment | Unique ID |
| name | varchar(255) | not null | Name |
| username | varchar(255) | not null | Username |
| password | varchar(255) | not null | Password |
| follower | int unsigned | not null, default to 0 | Follower Count |
| time | datetime | not null, default to current time | Signup Time |
### SQL statements:
```mysql
CREATE TABLE members (id BIGINT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255) NOT NULL,
username VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL,
follower INT UNSIGNED NOT NULL DEFAULT 0,
time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);
```
## Table: messages
| Column Name | Data Type | Additional Settings | Description |
| ----------- | --------- | ------------------- | ----------- |
| id | bigint | primary key, auto increment | Unique ID |
| members_id | bigint | not null, foreign key refer to id column in the member table | Member ID for Message Sender |
| content | varchar(255) | not null | Content |
| like_count | int unsigned | not null, default to 0 | Like Count |
| time | datetime | not null, default to current time | Publish Time |
### SQL statements:
```mysql
CREATE TABLE messages (id BIGINT PRIMARY KEY AUTO_INCREMENT, members_id BIGINT NOT NULL,
content VARCHAR(255) NOT NULL, like_count INT UNSIGNED NOT NULL DEFAULT 0,
time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY(members_id) REFERENCES members(id) ON DELETE CASCADE);
```
