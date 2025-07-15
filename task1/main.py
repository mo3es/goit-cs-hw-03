from program_files import create_db, seed, tasks_executor

# Database connection parameters
DB_HOST = (
    "postgres"  # Or your PostgreSQL server's IP/hostname (eg., 'your_remote_db.com')
)
DB_NAME = "rest_app"  # The name of your database
DB_USER = "postgres"  # Your PostgreSQL username
DB_PASS = "567234"  # Your PostgreSQL password
DB_PORT = "5432"  # Default PostgreSQL port
SCRIPT_NAME = "./queries/table_creation.sql"
SCRIPT2_NAME = "./queries/tasks_queries.sql"

# def connection_test():
#     try:
#         conn = psycopg2.connect(
#             host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
#         )

#         cur = conn.cursor()

#         print("Successfully connected to PostgreSQL!")

#     except psycopg2.Error as e:
#         print(f"Error connecting to PostgreSQL: {e}")

#     finally:
#         if cur:
#             cur.close()
#         if conn:
#             conn.close()
#         print("PostgreSQL connection closed.")


if __name__ == "__main__":
    create_db.create_db(DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT, SCRIPT_NAME)
    seed.insert_data_to_db(DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT)
    tasks_executor.execute_query(DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT, SCRIPT2_NAME)
