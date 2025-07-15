--- Table: users

DROP TABLE IF EXISTS  users CASCADE;
CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);


--- Table: task_status

DROP TABLE IF EXISTS task_status CASCADE; 
CREATE TABLE task_status(
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);


--- Table: tasks

DROP TABLE IF EXISTS tasks CASCADE;
CREATE TABLE tasks(
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    description TEXT,
    status_id INTEGER,
    FOREIGN KEY (status_id) REFERENCES task_status(id),
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
