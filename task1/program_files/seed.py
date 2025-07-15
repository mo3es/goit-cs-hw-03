import faker
import psycopg2
from random import randint


USERS_NUMBER = 20
TASK_NUMBER = 100
statuses = [("new",), ("in progress",), ("completed",)]
users, tasks = None, None


def generate_data(USERS_NUMBER, TASK_NUMBER):
    fake_users = []
    fake_tasks = []

    fake_data = faker.Faker()

    for _ in range(USERS_NUMBER):
        fake_users.append((fake_data.name(), fake_data.unique.email()))

    for _ in range(TASK_NUMBER):
        task = (
            fake_data.sentence(nb_words=randint(3, 8), variable_nb_words=True)[:-1],
            fake_data.paragraph(nb_sentences=randint(2, 5), variable_nb_sentences=True),
            randint(1, len(statuses)),
            randint(1, USERS_NUMBER),
        )
        fake_tasks.append(task)

    return fake_users, fake_tasks


def insert_data_to_db(DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT):
    with psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
    ) as conn:
        cur = conn.cursor()
        print("Succesfully connected to PostgeSQL'")
        users, tasks = generate_data(USERS_NUMBER, TASK_NUMBER)
        sql_to_statuses = """INSERT INTO task_status(name) VALUES (%s)"""
        sql_to_users = """INSERT INTO users(fullname, email) VALUES (%s, %s)"""
        sql_to_tasks = """INSERT INTO tasks(title, description, status_id, user_id) VALUES (%s, %s, %s, %s)"""
        cur.executemany(sql_to_statuses, statuses)
        print("Succesfully filled table 'task_statuses'")
        cur.executemany(sql_to_users, users)
        print("Succesfully filled table 'users'")
        cur.executemany(sql_to_tasks, tasks)
        print("Succesfully filled table 'tasks'")
        print("PostgreSQL connection closed.")
