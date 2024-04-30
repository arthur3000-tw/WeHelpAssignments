* Create a new database named website.
```mysql
CREATE DATABASE website;
```
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/16833a7a-65af-4671-b445-7461dc449b17)
* Create a new table named member, in the website database, designed as below:

| Colunm Name | Data Type | Additional Settings | Description |
| ----------- | --------- | ------------------- | ----------- |
| id | bigint | primary key, auto increment | Unique ID |
| name | varchar(255) | not null | Name |
| username | varchar(255) | not null | Username |
| password | varchar(255) | not null | Password |
| follower | int unsigned | not null, default to 0 | Follower Count |
| time | datetime | not null, default to current time | Signup Time |
```mysql
CREATE TABLE member (id BIGINT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255) NOT NULL, username VARCHAR(255) NOT NULL, follower INT UNSIGNED NOT NULL DEFAULT 0, time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);
```
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/39816a48-204f-4f24-ae0c-0043acbcd662)
![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/55860222-968a-437b-9dee-9cdbc2f1ef52)

