# Task 2: Create database and table in your MySQL server
## 1. Create a new database named website
### SQL statements:
```mysql
CREATE DATABASE website;
```
### Screenshot:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/16833a7a-65af-4671-b445-7461dc449b17)
## 2. Create a new table named member, in the website database, designed as below
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
CREATE TABLE member (id BIGINT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255) NOT NULL,
username VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL,
follower INT UNSIGNED NOT NULL DEFAULT 0,
time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);
```
### Screenshots:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/d7298a4f-cc07-4074-a24c-30c196f06fae)
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/afafd357-55e6-4e64-83cf-b35934d56870)
# Task 3: SQL CRUD
## 1. INSERT a new row to the member table where name, username and password must be set to test. INSERT additional 4 rows with arbitrary data
### SQL statements:
```mysql
INSERT INTO member (id, name, username, password)
VALUES (100, "test", "test", "test");
```
### Screenshots:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/01d0f297-c6ab-4515-9e85-6d93a38d20a6)
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/1895ec2d-db67-4af1-a11c-d58748944236)
### SQL statements:
```mysql
INSERT INTO member (id, name, username, password)
VALUES (101, "best","best","best"),
       (102, "john","john","john"),
       (103, "tom","tom","tom"),
       (104, "james","james","james");
```
### Screenshots:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/b5d75ebe-82a9-4d7c-8da1-baa25ed47c38)
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/e9501073-e5dc-40e8-b078-32c459b6cf21)
## 2. SELECT all rows from the member table
### SQL statements:
```mysql
SELECT * FROM member;
```
### Screenshot:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/e9501073-e5dc-40e8-b078-32c459b6cf21)
## 3. SELECT all rows from the member table, in descending order of time
### SQL statements:
```mysql
SELECT * FROM member
ORDER BY time DESC;
```
### Screenshot:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/f2c9d8f6-866f-42ef-bf14-359210288c06)
## 4. SELECT total 3 rows, second to fourth, from the member table, in descending order of time. Note: it does not mean SELECT rows where id are 2, 3, or 4
### SQL statements:
```mysql
SELECT * FROM member
ORDER BY time DESC
LIMIT 1, 3;
```
### Screenshot:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/0a6e18c1-6a7f-4704-a7ba-c56c450d748e)
## 5. SELECT rows where username equals to test
### SQL statements:
```mysql
SELECT * FROM member
WHERE username = "test";
```
### Screenshot:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/3d613f3c-2730-4914-8ce9-1e6b04531ab6)
## 6. SELECT rows where name includes the es keyword
### SQL statements:
```mysql
SELECT * FROM member
WHERE name LIKE "%es%";
```
### Screenshot:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/ee688c3a-e878-4391-be6e-6f95f572902b)
## 7. SELECT rows where both username and password equal to test
### SQL statements:
```mysql
SELECT * FROM member
WHERE username = "test" AND password = "test";
```
### Screenshot:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/7a619586-076e-472f-ac38-4bbc465d5db6)
## 8. UPDATE data in name column to test2 where username equals to test
### SQL statements:
```mysql
UPDATE member
SET name = "test2"
WHERE username = "test";
```
### Screenshots:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/070b9c47-262e-4e0e-bd9e-b73379f96b2c)
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/63f8922b-b378-4f2f-99be-c6ee5d03cb32)
# Task 4: SQL Aggregation Functions
## 1. SELECT how many rows from the member table
### SQL statements:
```mysql
SELECT COUNT(*)
FROM member;
```
### Screenshot:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/2a5505df-92fe-436d-8f66-1eafbe4bf40b)
## Update follower
```mysql
UPDATE member SET follower = 100 WHERE id = 101;
UPDATE member SET follower = 200 WHERE id = 102;
UPDATE member SET follower = 150 WHERE id = 103;
UPDATE member SET follower = 50 WHERE id = 104;
```
### Screenshots:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/2f735a5e-560f-4cf5-be64-ec45cc578b71)
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/203d5439-7551-470e-b329-848e1f1d28ec)
## 2. SELECT the sum of follower_count of all the rows from the member table
### SQL statements:
```mysql
SELECT SUM(follower) AS follower_count
FROM member;
```
### Screenshot:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/414ed144-f4b6-4666-a22b-24342cef99c4)
## 3. SELECT the average of follower_count of all the rows from the member table
### SQL statements:
```mysql
SELECT AVG(follower) AS follower_average
FROM member;
```
### Screenshot:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/31d2d413-4010-40f1-83c3-b688e7dc540f)
## 4. SELECT the average of follower_count of the first 2 rows, in descending order of follower_count, from the member table
### SQL statements:
```mysql
SELECT AVG(follower)
FROM (
SELECT follower FROM member
ORDER BY follower DESC
LIMIT 0, 2) AS follower_average;
```
### Screenshot:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/e51226f2-3bbf-4d00-8fc0-503a23a49950)
# Task 5: SQL JOIN
## 1. Create a new table named message, in the website database. designed as below
| Column Name | Data Type | Additional Settings | Description |
| ----------- | --------- | ------------------- | ----------- |
| id | bigint | primary key, auto increment | Unique ID |
| member_id | bigint | not null, foreign key refer to id column in the member table | Member ID for Message Sender |
| content | varchar(255) | not null | Content |
| like_count | int unsigned | not null, default to 0 | Like Count |
| time | datetime | not null, default to current time | Publish Time |
### SQL statements:
```mysql
CREATE TABLE message (id BIGINT PRIMARY KEY AUTO_INCREMENT, member_id BIGINT NOT NULL,
content VARCHAR(255) NOT NULL, like_count INT UNSIGNED NOT NULL DEFAULT 0,
time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY(member_id) REFERENCES member(id));
```
### Screenshots:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/7b71fe83-44b2-480f-b206-500411335b12)
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/1553400f-43ec-4229-a999-1189c7f22687)
## INSERT new data to message
### SQL statements:
```mysql
INSERT INTO message (id, member_id, content, like_count)
VALUES (10000, 100, "test test", 1),
       (10001, 103, "I am Tom", 18),
       (10002, 104, "King James!", 103),
       (10003, 102, "Little John", 7),
       (10004, 100, "test again", 3);
```
### Screenshots:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/dbf5a2ce-f234-4294-a051-301e85eb422d)
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/3044963c-6441-4ffd-bc46-e0c2d67d2960)
## 2. SELECT all messages, including sender names. We have to JOIN the member table to get that
### SQL statements:
```mysql
SELECT member.name, message.*
FROM message
JOIN member ON message.member_id = member.id;
```
### Screenshot:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/ef35e380-dd28-4070-bdeb-49ab53c07716)
## 3. SELECT all messages, including sender names, where sender username equals to test. We have to JOIN the member table to filter and get that
### SQL statements:
```mysql
SELECT member.name, message.* 
FROM message
JOIN member ON message.member_id = member.id
WHERE member.username = "test";
```
### Screenshot:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/07062ea6-9357-41f4-8d90-0b078677f220)
## 4. Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages where sender username equals to test
### SQL statements:
```mysql
SELECT member.username, AVG(message.like_count)
FROM message
JOIN member ON message.member_id = member.id
WHERE member.username = "test";
```
### Screenshot:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/fa5ee74b-7d48-44e0-8f8f-43c531a459e5)
## 5. Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages GROUP BY sender username
### SQL statements:
```mysql
SELECT member.username, AVG(message.like_count)
FROM message
JOIN member ON message.member_id = member.id
GROUP BY username;
```
### Screenshot:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/80bc540b-15bd-4f49-a0d7-be2a15e142dc)
# MySQL CREATE INDEX Statement
## CREATE INDEX
### SQL statements:
```mysql
CREATE INDEX idx_username_password ON member (username,password);
```
### Screenshot:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/f8244a5f-4609-4ff1-be31-eafcb3851902)
## Use EXPLAIN for SELECT ... WHERE ...
### SQL statements:
```mysql
EXPLAIN SELECT * FROM member WHERE username="test" AND password="test";
```
### Screenshot:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/6d5812a0-6812-42dd-b5cb-c5d37218af08)
### Without INDEX:
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/6ae09fbf-12b3-481a-8dc6-d7dfe33a6239)

