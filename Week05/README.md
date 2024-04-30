* Create a new database named website.

  SQL statements:
  ```mysql
  CREATE DATABASE website;
  ```
  Screenshot:
  
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

  SQL statements:
  ```mysql
  CREATE TABLE member (id BIGINT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255) NOT NULL,
  username VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL,
  follower INT UNSIGNED NOT NULL DEFAULT 0,
  time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);
  ```
  Screenshots:
  
  ![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/d7298a4f-cc07-4074-a24c-30c196f06fae)
  ![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/afafd357-55e6-4e64-83cf-b35934d56870)

* INSERT a new row to the member table where name, username and password must be set to test. INSERT additional 4 rows with arbitrary data.

  SQL statements:
  ```mysql
  INSERT INTO member (id, name, username, password)
  VALUES (100, "test", "test", "test");
  ```
  Screenshots:

  ![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/01d0f297-c6ab-4515-9e85-6d93a38d20a6)
  ![image](https://github.com/arthur3000-tw/WeHelpAssignments/assets/49877804/1895ec2d-db67-4af1-a11c-d58748944236)

