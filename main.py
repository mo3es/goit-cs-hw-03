from program_files import create_db, seed

# Database connection parameters
DB_HOST = (
    "postgres"  # Or your PostgreSQL server's IP/hostname (eg., 'your_remote_db.com')
)
DB_NAME = "rest_app"  # The name of your database
DB_USER = "postgres"  # Your PostgreSQL username
DB_PASS = "567234"  # Your PostgreSQL password
DB_PORT = "5432"  # Default PostgreSQL port
SCRIPT_NAME = "./queries/table_creation.sql"


# def connection_test():
#     # test connection

#     conn = None  # Initialize connection to None
#     cur = None  # Initialize cursor to None

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
