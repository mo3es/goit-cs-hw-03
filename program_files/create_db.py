import psycopg2


def create_db(DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT, script_name):
    with open(script_name, "r") as f:
        sql = f.read().split(";")
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
        )

        cur = conn.cursor()
        print("Successfully connected to PostgreSQL!")
        for statement in sql:
            statement = statement.strip()
            if statement:
                cur.execute(statement)
        conn.commit()
        print("Tables successfully created!")

    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        print("PostgreSQL connection closed.")
