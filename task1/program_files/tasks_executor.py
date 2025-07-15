import json
import psycopg2


def execute_query(DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT, script_name):
    with open(script_name, "r") as f:
        sql = f.read().split(";")

    conn = None
    cur = None
    results = []
    border = f"\n\n  {'-'*60} \n\n"
    with psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
    ) as conn:

        cur = conn.cursor()
        print("Successfully connected to PostgreSQL!")
        with open("./logfile.txt", "+a") as log:
            for statement in sql:
                statement = statement.strip()
                if statement:
                    cur.execute(statement)
                    if statement.strip().upper().startswith("SELECT"):
                        current = {statement: cur.fetchall()}
                    else:
                        current = {statement: "Done"}
                    results.append(current)
                    log.write(json.dumps(current))
                    log.write(border)
                    print(current)
                    print(border)
        print("Queries successfully done!")
        
            
        return results
